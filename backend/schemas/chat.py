# Pydantic models for chat data validation

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str
    timestamp: Optional[datetime] = None

class ChatSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None  # If users are authenticated
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class ChatDetail(BaseModel):
    session_id: str
    message: str
    chat_history: List[ChatMessage]
    response: str
    classification: dict
    rag_context: Optional[str] = None
    followup_questions: Optional[str] = None
    hashed_details: str  # Hashed version of the chat details
    created_at: datetime = datetime.utcnow()
