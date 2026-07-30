from typing import List
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.dependencies.db import get_session
from app.models.task import Task  # Apne Task model ke mutabik path verify kar lein
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter()

# 1. GET ALL TASKS FOR A USER (/api/{user_id}/tasks)
@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
async def get_tasks(user_id: UUID, session: Session = Depends(get_session)):
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks


# 2. CREATE A TASK FOR A USER (/api/{user_id}/tasks)
@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    user_id: UUID, 
    task_data: TaskCreate, 
    session: Session = Depends(get_session)
):
    # Task model ki field set karein
    new_task = Task(
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        user_id=user_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task


# 3. UPDATE A TASK (/api/{user_id}/tasks/{task_id})
@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
async def update_task(
    user_id: UUID,
    task_id: UUID,
    task_data: TaskUpdate,
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    existing_task = session.exec(statement).first()

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )

    # Sirf un fields ko update karein jo bhejiyen gayi hain
    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_task, key, value)

    existing_task.updated_at = datetime.utcnow()

    session.add(existing_task)
    session.commit()
    session.refresh(existing_task)
    return existing_task


# 4. DELETE A TASK (/api/{user_id}/tasks/{task_id})
@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    user_id: UUID,
    task_id: UUID,
    session: Session = Depends(get_session)
):
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    existing_task = session.exec(statement).first()

    if not existing_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )

    session.delete(existing_task)
    session.commit()
    return None