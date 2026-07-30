from typing import Dict, Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.db import get_session
# THEEK KIYA: get_current_user_id ko import kiya
from app.dependencies.auth import get_current_user_id 
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ErrorResponse
from app.services.ai.base import AbstractLLMService
from app.services.ai.gemini import GeminiLLMService
from app.services.chat import process_chat_message, LLMProcessingError, LLMValidationException

router = APIRouter()

# Dependency to provide LLM service.
def get_llm_service() -> AbstractLLMService:
    return GeminiLLMService()

@router.post("/chat/send-message")
async def send_chat_message(
    chat_request: ChatMessageRequest,
    # THEEK KIYA: User object ki jagah current_user_id (UUID) accept ki
    current_user_id: UUID = Depends(get_current_user_id),  
    session: Session = Depends(get_session),
    llm_service: AbstractLLMService = Depends(get_llm_service),
) -> ChatMessageResponse:
    """
    Endpoint for sending a message to the AI chatbot and receiving a response.
    The chatbot will process the message, potentially perform todo operations,
    and return a natural language response.
    """
    try:
        response_data = await process_chat_message(
            user_id=current_user_id, # THEEK KIYA: Seedha current_user_id pass kar di
            message_content=chat_request.message,
            session=session,
            llm_service=llm_service
        )
        return ChatMessageResponse(**response_data)
    except (LLMProcessingError, LLMValidationException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print(f"Unhandled error in send_chat_message: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal server error occurred."
        )