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
    sanitized_entities = {}

    if intent == "CREATE_TODO":
        title = entities.get("title")
        if not title or not isinstance(title, str) or len(title.strip()) == 0:
            raise LLMValidationException("CREATE_TODO intent requires a non-empty 'title'.")
        sanitized_entities["title"] = title.strip()

        if "due_date" in entities and entities["due_date"]:
            try:
                due_date_str = str(entities["due_date"]).lower()
                if due_date_str == "today":
                    sanitized_entities["due_date"] = date.today().isoformat()
                elif due_date_str == "tomorrow":
                    sanitized_entities["due_date"] = (date.today() + timedelta(days=1)).isoformat()
                elif re.match(r"^\d{4}-\d{2}-\d{2}$", due_date_str):
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
                UUID(str(target_id))
                sanitized_entities["target_id"] = str(target_id)
            except ValueError:
                raise LLMValidationException(f"Invalid 'target_id' format: {target_id}. Expected a valid UUID.")
        
        if target_title:
            sanitized_entities["target_title"] = str(target_title).strip()
        
        if intent == "UPDATE_TODO":
            status = entities.get("status")
            if status:
                if not isinstance(status, str) or status.lower() not in ["pending", "completed", "done"]:
                    raise LLMValidationException("UPDATE_TODO intent has invalid 'status'. Expected 'pending' or 'completed' or 'done'.")
                sanitized_entities["status"] = "completed" if status.lower() == "done" else status.lower()
            
            if "due_date" in entities and entities["due_date"]:
                try:
                    due_date_str = str(entities["due_date"]).lower()
                    if due_date_str == "today":
                        sanitized_entities["due_date"] = date.today().isoformat()
                    elif due_date_str == "tomorrow":
                        sanitized_entities["due_date"] = (date.today() + timedelta(days=1)).isoformat()
                    elif re.match(r"^\d{4}-\d{2}-\d{2}$", due_date_str):
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

    intent = "UNKNOWN"
    entities = {}
    response_text = "I'm sorry, I couldn't process your request at the moment. Please try again later."
    action_taken = "NO_ACTION"
    action_details = {}

    try:
        llm_raw_response = await llm_service.get_llm_response(prompt)
        
        if llm_raw_response and "error" in llm_raw_response:
            raise LLMProcessingError(llm_raw_response.get("details", "LLM returned an error."))

        intent = llm_raw_response.get("intent", "UNKNOWN")
        entities = llm_raw_response.get("entities", {})
        
        entities = _validate_and_sanitize_entities(intent, entities)

        if intent == "UNKNOWN":
            response_text = "I'm not sure how to help with that. Please try rephrasing your request or ask me to 'create', 'list', 'update', or 'delete' a todo."
        else:
            response_text = "Understood. Let me see what I can do."

    except (LLMValidationException, LLMProcessingError) as e:
        response_text = f"I'm having trouble understanding that: {e}"
        intent = "ERROR"
        entities = {"error": str(e)}
    except Exception as e:
        response_text = "An unexpected error occurred while processing your request."
        intent = "ERROR"
        entities = {"error": str(e)}

    try:
        if intent == "CREATE_TODO":
            todo_create = TaskCreate(
                title=entities.get("title"),
                description=entities.get("description"),
                due_date=entities.get("due_date"),
            )
            created_todo = crud_tasks.create_task(session=session, task_create=todo_create, user_id=user_id)
            response_text = f"I've added '{created_todo.title}' to your todo list."
            action_taken = "TODO_CREATED"
            action_details = created_todo.dict()
            
        elif intent == "LIST_TODOS":
            filter_status = entities.get("filter_status", "all")
            user_todos = crud_tasks.get_tasks_by_user(session=session, user_id=user_id)
            
            # Apply filtering in memory
            if filter_status == "pending":
                filtered_todos = [t for t in user_todos if not t.completed]
                response_text = f"You have {len(filtered_todos)} pending tasks:\n" + "\n".join([f"- {t.title}" for t in filtered_todos])
            elif filter_status == "completed":
                # 'Today' logic: check updated_at for today
                today = date.today()
                filtered_todos = [t for t in user_todos if t.completed and t.updated_at.date() == today]
                response_text = f"You have completed {len(filtered_todos)} tasks today:\n" + "\n".join([f"- {t.title}" for t in filtered_todos])
            else:
                response_text = "Here are your tasks:\n" + "\n".join([f"- {t.title} ({'Completed' if t.completed else 'Pending'})" for t in user_todos])
            
            action_taken = "TODO_LISTED"
            action_details = {"count": len(filtered_todos) if filter_status != "all" else len(user_todos)}
        
        elif intent == "UPDATE_TODO":
            target_id = entities.get("target_id")
            target_title = entities.get("target_title")
            
            # Find the task
            existing_task = None
            if target_id:
                existing_task = crud_tasks.get_task_by_id_and_user(session=session, task_id=UUID(target_id), user_id=user_id)
            elif target_title:
                tasks = crud_tasks.get_tasks_by_user(session=session, user_id=user_id)
                existing_task = next((t for t in tasks if t.title.lower() == target_title.lower()), None)
            
            if not existing_task:
                response_text = f"I couldn't find a todo item matching '{target_title or target_id}'."
                action_taken = "TODO_NOT_FOUND"
            else:
                update_data = {}
                if "status" in entities:
                    update_data["completed"] = entities["status"] == "completed"
                # Add other fields to update if needed
                
                updated_task = crud_tasks.update_task(session=session, task=existing_task, task_update=TaskUpdate(**update_data))
                response_text = f"I've updated '{updated_task.title}'."
                action_taken = "TODO_UPDATED"
                action_details = updated_task.dict()
                # Need to convert UUID to str in action_details if it is not JSON serializable, 
                # but dict() should handle it if defined correctly. 
                # Let's ensure it is serializable.
                if "id" in action_details:
                    action_details["id"] = str(action_details["id"])
                if "user_id" in action_details:
                    action_details["user_id"] = str(action_details["user_id"])

        elif intent == "DELETE_TODO":
            target_id = entities.get("target_id")
            target_title = entities.get("target_title")
            
            # Find the task
            existing_task = None
            if target_id:
                existing_task = crud_tasks.get_task_by_id_and_user(session=session, task_id=UUID(target_id), user_id=user_id)
            elif target_title:
                tasks = crud_tasks.get_tasks_by_user(session=session, user_id=user_id)
                existing_task = next((t for t in tasks if t.title.lower() == target_title.lower()), None)
            
            if not existing_task:
                response_text = f"I couldn't find a todo item matching '{target_title or target_id}' to delete."
                action_taken = "TODO_NOT_FOUND"
            else:
                crud_tasks.delete_task(session=session, task=existing_task)
                response_text = f"I've deleted '{existing_task.title}' from your todo list."
                action_taken = "TODO_DELETED"
                action_details = {"deleted_id": str(existing_task.id), "deleted_title": existing_task.title}

    except Exception as e:
        response_text = f"I encountered an error while performing that action."
        intent = "ERROR"
    
    create_chat_history_entry(
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
