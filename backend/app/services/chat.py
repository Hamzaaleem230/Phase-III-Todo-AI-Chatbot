from typing import Dict, Any, Optional
from uuid import UUID
from sqlmodel import Session
from datetime import datetime, date, timedelta
import re

from app.services.ai.base import AbstractLLMService
from app.services.ai.gemini import GeminiLLMService
from app.crud.chat import create_chat_history_entry
from app.crud import tasks as crud_tasks # Assuming existing todo CRUD operations
from app.schemas.task import TaskCreate # Assuming this exists for todo creation

class LLMProcessingError(Exception):
    """Custom exception for errors during LLM processing."""
    pass

class LLMValidationException(Exception):
    """Custom exception for validation errors in LLM extracted entities."""
    pass

def _validate_and_sanitize_entities(intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and sanitizes entities extracted from the LLM based on the detected intent.
    Raises LLMValidationException if entities are invalid for the given intent.
    """
    sanitized_entities = {}

    if intent == "CREATE_TODO":
        title = entities.get("title")
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise LLMValidationException("CREATE_TODO intent requires a non-empty 'title'.")
        sanitized_entities["title"] = title.strip()

        if "due_date" in entities and entities["due_date"]:
            try:
                # Attempt to parse various date formats
                due_date_str = str(entities["due_date"]).lower()
                if due_date_str == "today":
                    sanitized_entities["due_date"] = date.today().isoformat()
                elif due_date_str == "tomorrow":
                    sanitized_entities["due_date"] = (date.today() + timedelta(days=1)).isoformat()
                elif re.match(r"^\d{4}-\d{2}-\d{2}$", due_date_str): # YYYY-MM-DD
                    datetime.strptime(due_date_str, "%Y-%m-%d")
                    sanitized_entities["due_date"] = due_date_str
                else:
                    raise ValueError("Unsupported date format")
            except ValueError:
                raise LLMValidationException(f"Invalid 'due_date' format: {entities['due_date']}. Expected YYYY-MM-DD or 'today'/'tomorrow'.")
        
        if "description" in entities and entities["description"]:
            sanitized_entities["description"] = str(entities["description"]).strip()

    elif intent == "LIST_TODOS":
        filter_status = entities.get("filter_status", "all")
        if not isinstance(filter_status, str) or filter_status.lower() not in ["all", "pending", "completed"]:
            raise LLMValidationException("LIST_TODOS intent has invalid 'filter_status'. Expected 'all', 'pending', or 'completed'.")
        sanitized_entities["filter_status"] = filter_status.lower()

    elif intent in ["UPDATE_TODO", "DELETE_TODO"]:
        target_id = entities.get("target_id")
        target_title = entities.get("target_title")

        if not target_id and not target_title:
            raise LLMValidationException(f"{intent} intent requires either 'target_id' or 'target_title'.")
        
        if target_id:
            try:
                UUID(str(target_id)) # Validate it's a valid UUID
                sanitized_entities["target_id"] = str(target_id)
            except ValueError:
                raise LLMValidationException(f"Invalid 'target_id' format: {target_id}. Expected a valid UUID.")
        
        if target_title:
            sanitized_entities["target_title"] = str(target_title).strip()
        
        if intent == "UPDATE_TODO":
            status = entities.get("status")
            if status:
                if not isinstance(status, str) or status.lower() not in ["pending", "completed"]:
                    raise LLMValidationException("UPDATE_TODO intent has invalid 'status'. Expected 'pending' or 'completed'.")
                sanitized_entities["status"] = status.lower()
            
            if "due_date" in entities and entities["due_date"]:
                try:
                    due_date_str = str(entities["due_date"]).lower()
                    if due_date_str == "today":
                        sanitized_entities["due_date"] = date.today().isoformat()
                    elif due_date_str == "tomorrow":
                        sanitized_entities["due_date"] = (date.today() + timedelta(days=1)).isoformat()
                    elif re.match(r"^\d{4}-\d{2}-\d{2}$", due_date_str): # YYYY-MM-DD
                        datetime.strptime(due_date_str, "%Y-%m-%d")
                        sanitized_entities["due_date"] = due_date_str
                    else:
                        raise ValueError("Unsupported date format")
                except ValueError:
                    raise LLMValidationException(f"Invalid 'due_date' format: {entities['due_date']}. Expected YYYY-MM-DD or 'today'/'tomorrow'.")

    return sanitized_entities

async def process_chat_message(
    user_id: UUID, message_content: str, session: Session, llm_service: AbstractLLMService
) -> Dict[str, Any]:
    """
    Processes a user's chat message using an LLM, identifies intent,
    performs corresponding todo operations, and records chat history.
    """
    # 1. Construct prompt for LLM
    prompt = f"""
    You are an AI assistant that helps manage todo lists.
    Your task is to understand user commands related to todo items and extract structured JSON output.
    The output should contain an "intent" and "entities" dictionary.

    Available intents and their required entities:
    - CREATE_TODO: {{ "title": "str", "description": "Optional[str]", "due_date": "Optional[str]" }}
    - LIST_TODOS: {{ "filter_status": "Optional[str]" (e.g., "pending", "completed", "all") }}
    - UPDATE_TODO: {{ "target_id": "Optional[UUID]", "target_title": "Optional[str]", "status": "Optional[str]", "due_date": "Optional[str]" }}
    - DELETE_TODO: {{ "target_id": "Optional[UUID]", "target_title": "Optional[str]" }}
    - UNKNOWN: {{}} (if you cannot determine a clear intent or sufficient entities)

    Always respond ONLY with a JSON object. Ensure the JSON is valid and complete.

    Example interactions:
    User: "Add a todo to buy milk tomorrow"
    AI: {{"intent": "CREATE_TODO", "entities": {{"title": "buy milk", "due_date": "tomorrow"}}}}

    User: "Show my tasks"
    AI: {{"intent": "LIST_TODOS", "entities": {{"filter_status": "all"}}}}

    User: "Mark 'buy milk' as done"
    AI: {{"intent": "UPDATE_TODO", "entities": {{"target_title": "buy milk", "status": "done"}}}}

    User: "Delete the buy milk todo"
    AI: {{"intent": "DELETE_TODO", "entities": {{"target_title": "buy milk"}}}}

    User: "Hello"
    AI: {{"intent": "UNKNOWN", "entities": {{"greeting": true}}}}

    User message: "{message_content}"
    AI:
    """

    # 2. Get response from LLM
    llm_response_json = {}
    intent = "UNKNOWN"
    entities = {}
    response_text = "I'm sorry, I couldn't process your request at the moment. Please try again later."
    action_taken = "NO_ACTION"
    action_details = {}

    try:
        llm_raw_response = await llm_service.get_llm_response(prompt)
        
        if llm_raw_response and "error" in llm_raw_response:
            raise LLMProcessingError(llm_raw_response.get("details", "LLM returned an error."))

        llm_response_json = llm_raw_response
        intent = llm_response_json.get("intent", "UNKNOWN")
        entities = llm_response_json.get("entities", {})
        
        # Validate and sanitize entities
        entities = _validate_and_sanitize_entities(intent, entities)

        if intent == "UNKNOWN":
            response_text = "I'm not sure how to help with that. Please try rephrasing your request or ask me to 'create', 'list', 'update', or 'delete' a todo."
        else:
            response_text = "Understood. Let me see what I can do." # Generic initial response, will be updated by action logic

    except LLMValidationException as e:
        print(f"LLM Validation Error: {e}")
        response_text = f"I need a bit more clarity: {e}"
        intent = "ERROR" # Or a specific validation error intent
        entities = {"error": str(e)}
    except LLMProcessingError as e:
        print(f"LLM Processing Error: {e}")
        response_text = f"I'm having trouble understanding that: {e}"
        intent = "ERROR"
        entities = {"error": str(e)}
    except Exception as e:
        print(f"Unexpected error during LLM interaction or processing: {e}")
        response_text = "An unexpected error occurred while processing your request."
        intent = "ERROR"
        entities = {"error": str(e)}

    # 3. Perform action based on intent
    try:
        if intent == "CREATE_TODO":
            title = entities.get("title")
            description = entities.get("description")
            due_date = entities.get("due_date") # This is already sanitized to YYYY-MM-DD str
            
            todo_create = TaskCreate(
                title=title,
                description=description if description else None,
                due_date=due_date if due_date else None,
            )
            created_todo = await crud_tasks.create_task(session=session, task_create=todo_create, user_id=user_id)
            response_text = f"I've added '{created_todo.title}' to your todo list."
            if created_todo.due_date:
                response_text += f" It's due on {created_todo.due_date.strftime('%Y-%m-%d')}."
            action_taken = "TODO_CREATED"
            action_details = created_todo.dict()
            
        # Placeholder for other intents (LIST, UPDATE, DELETE)
        # These will be implemented in subsequent tasks
        elif intent == "LIST_TODOS":
            filter_status = entities.get("filter_status", "all")
            user_todos = await crud_tasks.get_user_tasks(session=session, user_id=user_id)
            
            filtered_todos = []
            if filter_status == "all":
                filtered_todos = user_todos
            elif filter_status == "pending":
                filtered_todos = [todo for todo in user_todos if todo.status == "pending"]
            elif filter_status == "completed":
                filtered_todos = [todo for todo in user_todos if todo.status == "completed"]

            if not filtered_todos:
                response_text = f"You have no {filter_status} todo items."
            else:
                todo_list_str = "\n".join([f"- {todo.title} (Status: {todo.status}, Due: {todo.due_date.strftime('%Y-%m-%d') if todo.due_date else 'N/A'})" for todo in filtered_todos])
                response_text = f"Here are your {filter_status} todo items:\n{todo_list_str}"
            action_taken = "TODO_LISTED"
            action_details = {"count": len(filtered_todos), "filter_status": filter_status}

        elif intent == "UPDATE_TODO":
            target_id = entities.get("target_id")
            target_title = entities.get("target_title")
            status = entities.get("status")
            due_date = entities.get("due_date")

            if target_id:
                existing_todo = await crud_tasks.get_task(session=session, task_id=UUID(target_id), user_id=user_id)
            elif target_title:
                existing_todo = await crud_tasks.get_task_by_title(session=session, title=target_title, user_id=user_id)
            else:
                raise LLMValidationException("UPDATE_TODO requires either 'target_id' or 'target_title'.")

            if not existing_todo:
                response_text = f"I couldn't find a todo item matching '{target_title or target_id}'."
                action_taken = "TODO_NOT_FOUND"
            else:
                todo_update_data = {}
                if status:
                    todo_update_data["status"] = status
                if due_date:
                    todo_update_data["due_date"] = due_date # This will be string, convert to date later if needed by crud.tasks.update_task
                
                updated_todo = await crud_tasks.update_task(session=session, task=existing_todo, task_in=todo_update_data) # Assuming task_in is Dict or TaskUpdate
                response_text = f"I've updated '{updated_todo.title}'. New status: {updated_todo.status}. New due date: {updated_todo.due_date.strftime('%Y-%m-%d') if updated_todo.due_date else 'N/A'}."
                action_taken = "TODO_UPDATED"
                action_details = updated_todo.dict()

        elif intent == "DELETE_TODO":
            target_id = entities.get("target_id")
            target_title = entities.get("target_title")

            if target_id:
                existing_todo = await crud_tasks.get_task(session=session, task_id=UUID(target_id), user_id=user_id)
            elif target_title:
                existing_todo = await crud_tasks.get_task_by_title(session=session, title=target_title, user_id=user_id)
            else:
                raise LLMValidationException("DELETE_TODO requires either 'target_id' or 'target_title'.")
            
            if not existing_todo:
                response_text = f"I couldn't find a todo item matching '{target_title or target_id}' to delete."
                action_taken = "TODO_NOT_FOUND"
            else:
                await crud_tasks.delete_task(session=session, task_id=existing_todo.id, user_id=user_id)
                response_text = f"I've deleted '{existing_todo.title}' from your todo list."
                action_taken = "TODO_DELETED"
                action_details = {"deleted_id": str(existing_todo.id), "deleted_title": existing_todo.title}

        elif intent == "UNKNOWN":
            pass # Handled above
        elif intent == "ERROR":
            pass # Handled above
            
    except LLMValidationException as e: # Catch validation errors specific to action execution
        print(f"Action Validation Error: {e}")
        response_text = f"I couldn't complete the action because: {e}"
        intent = "ERROR"
        entities = {"error": str(e)}
    except Exception as e:
        print(f"Error executing action for intent {intent}: {e}")
        response_text = f"I encountered an error while trying to perform that action. Please check your request."
        intent = "ERROR"
        entities = {"error": str(e)}
    
    # 4. Record chat history
    await create_chat_history_entry(
        session=session,
        user_id=user_id,
        message_content=message_content,
        response_content=response_text,
        intent_classified=intent,
        extracted_entities=entities
    )

    return {
        "response": response_text,
        "action_taken": action_taken,
        "action_details": action_details
    }

