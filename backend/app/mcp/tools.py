import os
from mcp.server.fastmcp import FastMCP
from uuid import UUID
from app.crud import tasks as crud_tasks
from app.schemas.task import TaskCreate, TaskUpdate
from app.db.database import get_session

# FastMCP initialized with "TodoAssistant"
mcp = FastMCP("TodoAssistant")

def get_session_context():
    return get_session()

@mcp.tool()
def list_tasks() -> list[dict]:
    """List all todo tasks for the authenticated user."""
    user_id = os.environ.get("USER_ID")
    if not user_id:
        raise ValueError("No authenticated user context.")
    session = get_session_context()
    tasks = crud_tasks.get_tasks_by_user(session=session, user_id=UUID(user_id))
    return [t.dict() for t in tasks]

@mcp.tool()
def add_task(title: str, description: str | None = None, due_date: str | None = None) -> dict:
    """Create a new todo task."""
    user_id = os.environ.get("USER_ID")
    if not user_id:
        raise ValueError("No authenticated user context.")
    session = get_session_context()
    task_create = TaskCreate(title=title, description=description, due_date=due_date)
    task = crud_tasks.create_task(session=session, task_create=task_create, user_id=UUID(user_id))
    return task.dict()

@mcp.tool()
def complete_task(task_id: str) -> dict:
    """Mark a task as completed."""
    user_id = os.environ.get("USER_ID")
    if not user_id:
        raise ValueError("No authenticated user context.")
    session = get_session_context()
    
    # Try lookup by UUID first, fallback to title search
    try:
        task = crud_tasks.get_task_by_id_and_user(session=session, task_id=UUID(task_id), user_id=UUID(user_id))
    except (ValueError, TypeError):
        # UUID conversion failed, try lookup by title
        tasks = crud_tasks.get_tasks_by_user(session=session, user_id=UUID(user_id))
        matching_tasks = [t for t in tasks if t.title.lower() == task_id.lower()]
        if not matching_tasks:
            raise ValueError(f"Task not found: {task_id}")
        
        # Sort by updated_at descending to pick the most recent one
        matching_tasks.sort(key=lambda t: t.updated_at, reverse=True)
        task = matching_tasks[0]
        
    if not task:
        raise ValueError("Task not found or unauthorized.")
    updated_task = crud_tasks.update_task(session=session, task=task, task_update=TaskUpdate(completed=True))
    return updated_task.dict()

@mcp.tool()
def delete_task(task_id: str) -> dict:
    """Delete a task."""
    user_id = os.environ.get("USER_ID")
    if not user_id:
        raise ValueError("No authenticated user context.")
    session = get_session_context()
    task = crud_tasks.get_task_by_id_and_user(session=session, task_id=UUID(task_id), user_id=UUID(user_id))
    if not task:
        raise ValueError("Task not found or unauthorized.")
    crud_tasks.delete_task(session=session, task=task)
    return {"status": "deleted", "task_id": task_id}

@mcp.tool()
def update_task(task_id: str, title: str | None = None, description: str | None = None, due_date: str | None = None, completed: bool | None = None) -> dict:
    """Update an existing task."""
    user_id = os.environ.get("USER_ID")
    if not user_id:
        raise ValueError("No authenticated user context.")
    session = get_session_context()
    task = crud_tasks.get_task_by_id_and_user(session=session, task_id=UUID(task_id), user_id=UUID(user_id))
    if not task:
        raise ValueError("Task not found or unauthorized.")
    
    update_data = TaskUpdate(title=title, description=description, due_date=due_date, completed=completed)
    updated_task = crud_tasks.update_task(session=session, task=task, task_update=update_data)
    return updated_task.dict()
