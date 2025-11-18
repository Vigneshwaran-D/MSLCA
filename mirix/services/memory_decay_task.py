"""
Memory Decay Task for Background Deletion of Low-Importance Memories

This module provides functionality to periodically identify and delete memories
that have fallen below temporal relevance thresholds or exceeded maximum age limits.
"""

from datetime import datetime, timezone
from typing import Dict, List

from mirix.log import get_logger
from mirix.orm.chat_message import ChatMessage
from mirix.orm.episodic_memory import EpisodicEvent
from mirix.orm.knowledge_vault import KnowledgeVaultItem
from mirix.orm.procedural_memory import ProceduralMemoryItem
from mirix.orm.resource_memory import ResourceMemoryItem
from mirix.orm.semantic_memory import SemanticMemoryItem
from mirix.services.temporal_reasoning_service import temporal_service
from mirix.settings import temporal_settings

logger = get_logger(__name__)

# Memory types to process (including chat messages)
MEMORY_TYPES = [
    ChatMessage,
    EpisodicEvent,
    SemanticMemoryItem,
    ProceduralMemoryItem,
    ResourceMemoryItem,
    KnowledgeVaultItem,
]


class MemoryDecayTask:
    """
    Background task for identifying and deleting forgotten memories.

    This task runs periodically to:
    1. Identify memories that should be forgotten based on temporal criteria
    2. Delete low-importance, old, or irrelevant memories
    3. Log statistics about memory cleanup
    """

    def __init__(self):
        """Initialize the memory decay task."""
        self.logger = logger

    def run_decay_cycle(
        self,
        session,
        organization_id: str,
        user_id: str = None,
        dry_run: bool = False,
    ) -> Dict[str, int]:
        """
        Run a complete decay cycle for all memory types.

        Args:
            session: Database session
            organization_id: Organization ID to filter memories by
            user_id: Optional user ID to filter memories by
            dry_run: If True, identify but don't delete memories

        Returns:
            Dictionary with deletion statistics per memory type
        """
        if not temporal_settings.enabled:
            self.logger.info("Temporal reasoning is disabled, skipping decay cycle")
            return {}

        self.logger.info(
            f"Starting memory decay cycle for organization {organization_id}"
            + (f", user {user_id}" if user_id else "")
        )

        current_time = datetime.now(timezone.utc)
        stats = {}

        for memory_type in MEMORY_TYPES:
            type_name = memory_type.__name__
            self.logger.info(f"Processing {type_name}...")

            try:
                # Identify forgettable memories
                forgettable_memories = temporal_service.identify_forgettable_memories(
                    session=session,
                    memory_type=memory_type,
                    organization_id=organization_id,
                    user_id=user_id,
                    current_time=current_time,
                    limit=1000,  # Process up to 1000 per type per cycle
                )

                if not forgettable_memories:
                    self.logger.info(f"No forgettable {type_name} found")
                    stats[type_name] = 0
                    continue

                self.logger.info(
                    f"Found {len(forgettable_memories)} forgettable {type_name}"
                )

                if dry_run:
                    self.logger.info(f"[DRY RUN] Would delete {len(forgettable_memories)} {type_name}")
                    for memory, reason in forgettable_memories[:10]:  # Log first 10
                        self.logger.info(f"[DRY RUN]   - {memory.id}: {reason}")
                    if len(forgettable_memories) > 10:
                        self.logger.info(
                            f"[DRY RUN]   ... and {len(forgettable_memories) - 10} more"
                        )
                    stats[type_name] = len(forgettable_memories)
                else:
                    # Delete forgettable memories
                    deleted_count = temporal_service.delete_forgettable_memories(
                        session=session,
                        forgettable_memories=forgettable_memories,
                    )

                    # Commit deletions
                    session.commit()

                    self.logger.info(f"Deleted {deleted_count} {type_name}")
                    stats[type_name] = deleted_count

            except Exception as e:
                self.logger.error(f"Error processing {type_name}: {e}", exc_info=True)
                session.rollback()
                stats[type_name] = -1  # Indicate error

        total_deleted = sum(count for count in stats.values() if count > 0)
        self.logger.info(
            f"Memory decay cycle completed: {total_deleted} memories deleted"
        )

        return stats

    def run_decay_for_all_users(
        self,
        session,
        organization_id: str,
        dry_run: bool = False,
    ) -> Dict[str, Dict[str, int]]:
        """
        Run decay cycle for all users in an organization.

        Args:
            session: Database session
            organization_id: Organization ID
            dry_run: If True, identify but don't delete memories

        Returns:
            Dictionary mapping user IDs to their deletion statistics
        """
        if not temporal_settings.enabled:
            self.logger.info("Temporal reasoning is disabled, skipping decay")
            return {}

        self.logger.info(
            f"Starting organization-wide memory decay for {organization_id}"
        )

        # Get all users in the organization
        from mirix.orm.user import User

        users = session.query(User).filter(
            User.organization_id == organization_id
        ).all()

        all_stats = {}
        for user in users:
            self.logger.info(f"Processing user {user.id}...")
            user_stats = self.run_decay_cycle(
                session=session,
                organization_id=organization_id,
                user_id=user.id,
                dry_run=dry_run,
            )
            all_stats[user.id] = user_stats

        self.logger.info("Organization-wide memory decay completed")
        return all_stats

    def get_decay_statistics(
        self,
        session,
        organization_id: str,
        user_id: str = None,
    ) -> Dict[str, Dict]:
        """
        Get statistics about memories eligible for decay without deleting.

        Args:
            session: Database session
            organization_id: Organization ID
            user_id: Optional user ID to filter by

        Returns:
            Dictionary with statistics per memory type
        """
        if not temporal_settings.enabled:
            return {}

        current_time = datetime.now(timezone.utc)
        stats = {}

        for memory_type in MEMORY_TYPES:
            type_name = memory_type.__name__

            try:
                forgettable = temporal_service.identify_forgettable_memories(
                    session=session,
                    memory_type=memory_type,
                    organization_id=organization_id,
                    user_id=user_id,
                    current_time=current_time,
                    limit=1000,
                )

                # Categorize by reason
                reasons = {}
                for memory, reason in forgettable:
                    if reason not in reasons:
                        reasons[reason] = 0
                    reasons[reason] += 1

                stats[type_name] = {
                    "total_forgettable": len(forgettable),
                    "reasons": reasons,
                }

            except Exception as e:
                self.logger.error(
                    f"Error getting statistics for {type_name}: {e}",
                    exc_info=True,
                )
                stats[type_name] = {"error": str(e)}

        return stats


# Singleton instance
memory_decay_task = MemoryDecayTask()

