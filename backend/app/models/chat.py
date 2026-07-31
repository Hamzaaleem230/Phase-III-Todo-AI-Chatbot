from datetime import datetime, timezone
from typing import Optional, Dict, Any
from uuid import UUID, uuid4

# THEEK KIYA: Column import kiya SQLAlchemy se taake JSONB type sahi se assign ho sake
from sqlmodel import Field, SQLModel, Column 
from sqlalchemy.dialects.postgresql import JSONB

from app.models.user import User # Keep this import for ForeignKey reference

class ChatHistoryBase(SQLModel):
    user_id: UUID = Field(foreign_key="users.id", index=True)
    message_content: str = Field(index=False)
    response_content: str = Field(index=False)
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    intent_classified: Optional[str] = Field(default=None, index=True, max_length=50)
    
    # THEEK KIYA: sa_column_kwargs ki jagah seedha sa_column=Column(JSONB) use kiya hai
    extracted_entities: Dict[str, Any] = Field(
        default_factory=dict, 
        sa_column=Column(JSONB, nullable=False, server_default='{}')
    )

class ChatHistory(ChatHistoryBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True, index=True)