from datetime import datetime
from typing import Dict, Optional

from pydantic import Field

from mirix.schemas.mirix_base import MirixBase


class ChatMessageCreate(MirixBase):
    """Schema for creating a new chat message"""

    session_id: str = Field(..., description="Chat session ID")
    role: str = Field(..., description="Role: user, assistant, or system")
    content: str = Field(..., description="Message content")
    agent_id: Optional[str] = Field(None, description="Agent ID if assistant message")
    parent_message_id: Optional[str] = Field(None, description="Parent message ID")
    metadata_: Optional[Dict] = Field(default_factory=dict, description="Additional metadata")
    importance_score: Optional[float] = Field(0.5, description="Initial importance score")


class ChatMessage(MirixBase):
    """Schema for a chat message"""

    id: str = Field(..., description="Message ID")
    session_id: str = Field(..., description="Chat session ID")
    role: str = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    created_at: datetime = Field(..., description="Creation timestamp")
    
    # Temporal fields
    access_count: int = Field(0, description="Access count")
    last_accessed_at: Optional[datetime] = Field(None, description="Last access time")
    importance_score: float = Field(0.5, description="Importance score")
    rehearsal_count: int = Field(0, description="Rehearsal count")
    
    # Optional fields
    agent_id: Optional[str] = Field(None, description="Agent ID")
    parent_message_id: Optional[str] = Field(None, description="Parent message ID")
    metadata_: Optional[Dict] = Field(default_factory=dict, description="Metadata")
    last_modify: Optional[Dict] = Field(None, description="Last modification info")
    
    # Organization and user
    organization_id: str = Field(..., description="Organization ID")
    user_id: str = Field(..., description="User ID")

    class Config:
        from_attributes = True


class ChatSession(MirixBase):
    """Schema for a chat session summary"""

    session_id: str = Field(..., description="Session ID")
    message_count: int = Field(..., description="Number of messages")
    first_message_at: datetime = Field(..., description="First message timestamp")
    last_message_at: datetime = Field(..., description="Last message timestamp")
    avg_importance: float = Field(..., description="Average importance score")
    total_tokens: Optional[int] = Field(None, description="Total tokens used")

