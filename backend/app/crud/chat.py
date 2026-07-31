from typing import Optional, Dict, Any
from uuid import UUID
from sqlmodel import Session, select

from app.models.chat import ChatHistory
from app.schemas.chat import ChatMessageResponse

def create_chat_history_entry(
    session: Session,
    user_id: UUID,
    message_content: str,
    response_content: str,
    intent_classified: Optional[str] = None,
    extracted_entities: Optional[Dict[str, Any]] = None,
) -> ChatHistory:
    """
    Creates a new chat history entry in the database.
    """
    db_chat_entry = ChatHistory(
        user_id=user_id,
        message_content=message_content,
        response_content=response_content,
        intent_classified=intent_classified,
        extracted_entities=extracted_entities,
    )
    session.add(db_chat_entry)
    session.commit()
    session.refresh(db_chat_entry)
    return db_chat_entry

def get_chat_history_by_user(
    session: Session, user_id: UUID, skip: int = 0, limit: int = 100
) -> list[ChatHistory]:
    """
    Retrieves chat history entries for a specific user.
    """
    statement = select(ChatHistory).where(ChatHistory.user_id == user_id).offset(skip).limit(limit)
    result = session.exec(statement)
    return result.all()
