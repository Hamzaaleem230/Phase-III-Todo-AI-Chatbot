from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field

# Request schema for sending a message to the chatbot
class ChatMessageRequest(BaseModel):
    message: str = Field(..., description="The user's natural language input message.")

# Response schema for the chatbot's reply
class ChatMessageResponse(BaseModel):
    response: str = Field(..., description="The AI's natural language response.")
    action_taken: Optional[str] = Field(None, description="Optional. Indicates the type of action performed (e.g., TODO_CREATED, TODO_LISTED, NO_ACTION).")
    action_details: Optional[Dict[str, Any]] = Field(None, description="Optional. JSON details of the action, such as todo_id, title, etc.")

# Schema for error responses (as defined in API contract)
class ChatHistoryResponse(BaseModel):
    id: UUID
    user_id: UUID
    message_content: str
    response_content: str
    timestamp: datetime
    intent_classified: Optional[str]
    extracted_entities: Dict[str, Any]
