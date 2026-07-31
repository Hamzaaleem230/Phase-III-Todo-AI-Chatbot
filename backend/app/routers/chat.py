from typing import Dict, Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.dependencies.db import get_session
from app.dependencies.auth import get_current_user_id 
from app.schemas.chat import ChatMessageRequest, ChatMessageResponse, ChatHistoryResponse
from app.services.ai.base import AbstractLLMService
from app.services.ai.gemini import GeminiLLMService
from app.services.chat import process_chat_message, LLMProcessingError, LLMValidationException
from app.crud.chat import get_chat_history_by_user

router = APIRouter()

# Dependency to provide LLM service.
def get_llm_service() -> AbstractLLMService:
    return GeminiLLMService()

@router.get("/chat/history", response_model=List[ChatHistoryResponse])
async def get_chat_history(
    current_user_id: UUID = Depends(get_current_user_id),
    session: Session = Depends(get_session),
):
    """
    Endpoint to retrieve the chat history for the authenticated user.
    """
    history = get_chat_history_by_user(session=session, user_id=current_user_id)
    return history

import traceback

@router.post("/chat/send-message")
async def send_chat_message(
    chat_request: ChatMessageRequest,
    current_user_id: UUID = Depends(get_current_user_id),  
    session: Session = Depends(get_session),
    llm_service: AbstractLLMService = Depends(get_llm_service),
) -> ChatMessageResponse:
    """
    Endpoint for sending a message to the AI chatbot and receiving a response.
    """
    print("\n>>> Entering send_chat_message endpoint")
    print(f">>> Authenticated user: {current_user_id}")
    try:
        print(">>> Before process_chat_message()")
        response_data = await process_chat_message(
            user_id=current_user_id,
            message_content=chat_request.message,
            session=session,
            llm_service=llm_service
        )
        print(">>> After process_chat_message()")
        print(">>> Before ChatMessageResponse(...)")
        result = ChatMessageResponse(**response_data)
        print(">>> Before return")
        return result
    except (LLMProcessingError, LLMValidationException) as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        print("\n========== FULL TRACEBACK ==========")
        print(traceback.format_exc())
        print("====================================")
        raise