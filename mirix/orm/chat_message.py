import datetime as dt
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, Column, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, declared_attr, mapped_column, relationship

from mirix.constants import MAX_EMBEDDING_DIM
from mirix.orm.custom_columns import CommonVector, EmbeddingConfigColumn
from mirix.orm.mixins import OrganizationMixin, UserMixin
from mirix.orm.sqlalchemy_base import SqlalchemyBase
from mirix.schemas.chat_message import ChatMessage as PydanticChatMessage
from mirix.settings import settings

if TYPE_CHECKING:
    from mirix.orm.organization import Organization
    from mirix.orm.user import User


class ChatMessage(SqlalchemyBase, OrganizationMixin, UserMixin):
    """
    Stores chat conversation messages with temporal reasoning capabilities.
    
    Each message is treated as an episodic memory that can be retrieved,
    rehearsed, and eventually forgotten based on temporal decay.
    """

    __tablename__ = "chat_messages"
    __pydantic_model__ = PydanticChatMessage

    # Primary key
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        doc="Unique ID for this chat message",
    )

    # Session tracking
    session_id: Mapped[str] = mapped_column(
        String,
        nullable=False,
        index=True,
        doc="Chat session ID for grouping related messages",
    )

    # Message content
    role: Mapped[str] = mapped_column(
        String,
        nullable=False,
        doc="Role of the message sender (user, assistant, system)",
    )

    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        doc="The actual message content",
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(dt.timezone.utc),
        nullable=False,
        doc="When this message was created",
    )

    # Temporal reasoning fields
    access_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of times this message has been accessed/retrieved",
    )

    last_accessed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
        default=None,
        doc="Timestamp of the last access/retrieval of this message",
    )

    importance_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0.5,
        doc="Base importance score (0-1) affecting decay rate",
    )

    rehearsal_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        doc="Number of times this message has been rehearsed/strengthened",
    )

    # Metadata
    metadata_: Mapped[dict] = mapped_column(
        JSON,
        default=dict,
        nullable=True,
        doc="Additional metadata (tokens, model, context, etc.)",
    )

    # Agent information
    agent_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
        doc="ID of the agent that generated this message (if assistant role)",
    )

    # Conversation context
    parent_message_id: Mapped[str] = mapped_column(
        String,
        nullable=True,
        doc="ID of the parent message (for threading)",
    )

    # Search and retrieval
    embedding_config: Mapped[Optional[dict]] = mapped_column(
        EmbeddingConfigColumn, nullable=True, doc="Embedding configuration"
    )

    # Vector embedding field based on database type
    if settings.mirix_pg_uri_no_default:
        from pgvector.sqlalchemy import Vector

        content_embedding = mapped_column(Vector(MAX_EMBEDDING_DIM), nullable=True)
    else:
        content_embedding = Column(CommonVector, nullable=True)

    # Modification tracking
    last_modify: Mapped[dict] = mapped_column(
        JSON,
        nullable=False,
        default=lambda: {
            "timestamp": datetime.now(dt.timezone.utc).isoformat(),
            "operation": "created",
        },
        doc="Last modification info including timestamp and operation type",
    )

    @declared_attr
    def organization(cls) -> Mapped["Organization"]:
        """Relationship to the Organization that owns this message."""
        return relationship(
            "Organization", back_populates="chat_messages", lazy="selectin"
        )

    @declared_attr
    def user(cls) -> Mapped["User"]:
        """Relationship to the User that owns this message."""
        return relationship("User", lazy="selectin")

