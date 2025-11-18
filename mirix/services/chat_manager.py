"""
Chat Manager Service

Handles chat message storage, retrieval, and integration with temporal reasoning.
All chat messages are treated as episodic memories subject to decay and rehearsal.
"""

import datetime as dt
import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import desc, func, select

from mirix.constants import BUILD_EMBEDDINGS_FOR_MEMORY
from mirix.embeddings import embedding_model
from mirix.log import get_logger
from mirix.orm.chat_message import ChatMessage
from mirix.schemas.chat_message import (
    ChatMessage as PydanticChatMessage,
    ChatMessageCreate,
    ChatSession,
)
from mirix.schemas.user import User as PydanticUser
from mirix.services.temporal_reasoning_service import temporal_service
from mirix.settings import temporal_settings
from mirix.utils import enforce_types, generate_unique_short_id

logger = get_logger(__name__)


class ChatManager:
    """Manager for chat messages with temporal reasoning integration"""

    def __init__(self):
        from mirix.server.server import db_context

        self.session_maker = db_context

    @enforce_types
    def create_message(
        self,
        actor: PydanticUser,
        message_data: ChatMessageCreate,
        embedding_config: Optional[dict] = None,
    ) -> PydanticChatMessage:
        """
        Create a new chat message with temporal fields.

        Args:
            actor: User creating the message
            message_data: Message creation data
            embedding_config: Optional embedding configuration

        Returns:
            Created chat message
        """
        with self.session_maker() as session:
            # Generate message ID
            message_id = generate_unique_short_id(
                self.session_maker, ChatMessage, prefix="chat-msg", length=8
            )

            # Create embedding if configured
            content_embedding = None
            if BUILD_EMBEDDINGS_FOR_MEMORY and embedding_config:
                try:
                    embedding_result = embedding_model(embedding_config).get_text_embedding(
                        message_data.content
                    )
                    content_embedding = embedding_result
                except Exception as e:
                    logger.error(f"Error creating embedding for chat message: {e}")

            # Create chat message
            chat_message = ChatMessage(
                id=message_id,
                session_id=message_data.session_id,
                role=message_data.role,
                content=message_data.content,
                agent_id=message_data.agent_id,
                parent_message_id=message_data.parent_message_id,
                metadata_=message_data.metadata_ or {},
                importance_score=message_data.importance_score,
                organization_id=actor.organization_id,
                user_id=actor.id,
                embedding_config=embedding_config,
                content_embedding=content_embedding,
            )

            session.add(chat_message)
            session.commit()
            session.refresh(chat_message)

            logger.info(f"Created chat message {message_id} in session {message_data.session_id}")

            return chat_message.to_pydantic()

    @enforce_types
    def get_session_messages(
        self,
        actor: PydanticUser,
        session_id: str,
        limit: Optional[int] = 100,
        include_system: bool = True,
    ) -> List[PydanticChatMessage]:
        """
        Retrieve messages from a chat session.

        Args:
            actor: User requesting messages
            session_id: Chat session ID
            limit: Maximum number of messages to return
            include_system: Whether to include system messages

        Returns:
            List of chat messages
        """
        with self.session_maker() as session:
            query = (
                select(ChatMessage)
                .where(
                    ChatMessage.session_id == session_id,
                    ChatMessage.user_id == actor.id,
                )
                .order_by(ChatMessage.created_at.asc())
            )

            if not include_system:
                query = query.where(ChatMessage.role != "system")

            if limit:
                query = query.limit(limit)

            result = session.execute(query)
            messages = result.scalars().all()

            # Track access for temporal reasoning
            if temporal_settings.enabled:
                current_time = datetime.now(dt.timezone.utc)
                for msg in messages:
                    temporal_service.track_access(msg, session)

                session.commit()

            return [msg.to_pydantic() for msg in messages]

    @enforce_types
    def get_recent_context(
        self,
        actor: PydanticUser,
        session_id: str,
        limit: int = 10,
    ) -> List[PydanticChatMessage]:
        """
        Get recent messages for context with temporal scoring.

        Args:
            actor: User requesting context
            session_id: Chat session ID
            limit: Number of recent messages

        Returns:
            List of recent messages sorted by temporal relevance
        """
        with self.session_maker() as session:
            # Get recent messages
            query = (
                select(ChatMessage)
                .where(
                    ChatMessage.session_id == session_id,
                    ChatMessage.user_id == actor.id,
                )
                .order_by(ChatMessage.created_at.desc())
                .limit(limit * 2)  # Get more for scoring
            )

            result = session.execute(query)
            messages = list(result.scalars().all())

            if not temporal_settings.enabled or not messages:
                return [msg.to_pydantic() for msg in messages[:limit]]

            # Apply temporal scoring
            current_time = datetime.now(dt.timezone.utc)
            scored_messages = []

            for msg in messages:
                temporal_score = temporal_service.calculate_temporal_score(
                    msg, current_time
                )
                scored_messages.append((temporal_score, msg))

                # Track access
                temporal_service.track_access(msg, session)

            # Sort by temporal score
            scored_messages.sort(key=lambda x: x[0], reverse=True)

            # Commit access tracking
            session.commit()

            # Return top messages
            return [msg.to_pydantic() for score, msg in scored_messages[:limit]]

    @enforce_types
    def search_messages(
        self,
        actor: PydanticUser,
        query_text: str,
        session_id: Optional[str] = None,
        limit: int = 20,
    ) -> List[PydanticChatMessage]:
        """
        Search chat messages with temporal scoring.

        Args:
            actor: User performing search
            query_text: Search query
            session_id: Optional session ID to filter by
            limit: Maximum results

        Returns:
            List of matching messages
        """
        with self.session_maker() as session:
            # Build query
            query = select(ChatMessage).where(ChatMessage.user_id == actor.id)

            if session_id:
                query = query.where(ChatMessage.session_id == session_id)

            # Simple text search (can be enhanced with FTS or embeddings)
            query = query.where(
                func.lower(ChatMessage.content).contains(query_text.lower())
            )

            result = session.execute(query)
            messages = list(result.scalars().all())

            if not temporal_settings.enabled or not messages:
                return [msg.to_pydantic() for msg in messages[:limit]]

            # Apply temporal scoring
            current_time = datetime.now(dt.timezone.utc)
            scored_messages = []

            for msg in messages:
                temporal_score = temporal_service.calculate_temporal_score(
                    msg, current_time
                )
                # Boost score if query matches well (simple heuristic)
                relevance = query_text.lower() in msg.content.lower()
                combined_score = temporal_score * (2.0 if relevance else 1.0)

                scored_messages.append((combined_score, msg))

                # Track access
                temporal_service.track_access(msg, session)

                # Rehearse if high relevance
                if temporal_service.should_rehearse(msg, combined_score):
                    temporal_service.rehearse_memory(msg, session)

            # Sort by combined score
            scored_messages.sort(key=lambda x: x[0], reverse=True)

            # Commit changes
            session.commit()

            return [msg.to_pydantic() for score, msg in scored_messages[:limit]]

    @enforce_types
    def get_session_summary(
        self,
        actor: PydanticUser,
        session_id: str,
    ) -> Optional[ChatSession]:
        """
        Get summary statistics for a chat session.

        Args:
            actor: User requesting summary
            session_id: Chat session ID

        Returns:
            Chat session summary or None
        """
        with self.session_maker() as session:
            query = select(ChatMessage).where(
                ChatMessage.session_id == session_id,
                ChatMessage.user_id == actor.id,
            )

            result = session.execute(query)
            messages = result.scalars().all()

            if not messages:
                return None

            # Calculate summary
            message_count = len(messages)
            first_message_at = min(msg.created_at for msg in messages)
            last_message_at = max(msg.created_at for msg in messages)
            avg_importance = sum(msg.importance_score for msg in messages) / message_count

            # Calculate total tokens if available
            total_tokens = sum(
                msg.metadata_.get("tokens", 0)
                for msg in messages
                if msg.metadata_
            )

            return ChatSession(
                session_id=session_id,
                message_count=message_count,
                first_message_at=first_message_at,
                last_message_at=last_message_at,
                avg_importance=avg_importance,
                total_tokens=total_tokens if total_tokens > 0 else None,
            )

    @enforce_types
    def list_sessions(
        self,
        actor: PydanticUser,
        limit: int = 50,
    ) -> List[ChatSession]:
        """
        List all chat sessions for a user.

        Args:
            actor: User requesting sessions
            limit: Maximum sessions to return

        Returns:
            List of chat session summaries
        """
        with self.session_maker() as session:
            # Get all unique session IDs
            query = (
                select(ChatMessage.session_id)
                .where(ChatMessage.user_id == actor.id)
                .distinct()
                .order_by(desc(ChatMessage.created_at))
                .limit(limit)
            )

            result = session.execute(query)
            session_ids = [row[0] for row in result.all()]

            # Get summary for each session
            summaries = []
            for session_id in session_ids:
                summary = self.get_session_summary(actor, session_id)
                if summary:
                    summaries.append(summary)

            return summaries

    @enforce_types
    def delete_old_messages(
        self,
        actor: PydanticUser,
        session_id: Optional[str] = None,
        dry_run: bool = True,
    ) -> int:
        """
        Delete chat messages based on temporal criteria.

        Args:
            actor: User performing deletion
            session_id: Optional session ID to filter
            dry_run: If True, only count deletions

        Returns:
            Number of messages deleted (or would be deleted)
        """
        with self.session_maker() as session:
            current_time = datetime.now(dt.timezone.utc)
            
            # Build query
            query = select(ChatMessage).where(ChatMessage.user_id == actor.id)
            
            if session_id:
                query = query.where(ChatMessage.session_id == session_id)
            
            result = session.execute(query)
            messages = result.scalars().all()
            
            # Identify forgettable messages
            to_delete = []
            for msg in messages:
                should_delete, reason = temporal_service.should_delete(msg, current_time)
                if should_delete:
                    to_delete.append(msg)
                    logger.info(f"Chat message {msg.id} marked for deletion: {reason}")
            
            if dry_run:
                return len(to_delete)
            
            # Actually delete
            for msg in to_delete:
                session.delete(msg)
            
            session.commit()
            logger.info(f"Deleted {len(to_delete)} chat messages")
            
            return len(to_delete)


# Singleton instance
chat_manager = ChatManager()

