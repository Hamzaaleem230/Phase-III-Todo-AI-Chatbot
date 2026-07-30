from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str | None = None
    completed: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ChatMessage(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    role: str   # user | assistant
    content: str
    created_at: datetime = Field(default_factory=datetime.utcnow)