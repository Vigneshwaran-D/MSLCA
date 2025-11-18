"""
Temporal Reasoning Service for Memory Decay Modeling

This service implements hybrid decay functions (exponential + power law) for memory
importance scoring, rehearsal strengthening, and forgetting mechanisms.
"""

import math
from datetime import datetime, timezone
from typing import Any, List, Optional, Tuple, Union

from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from mirix.log import get_logger
from mirix.orm.episodic_memory import EpisodicEvent
from mirix.orm.knowledge_vault import KnowledgeVaultItem
from mirix.orm.procedural_memory import ProceduralMemoryItem
from mirix.orm.resource_memory import ResourceMemoryItem
from mirix.orm.semantic_memory import SemanticMemoryItem
from mirix.settings import temporal_settings

logger = get_logger(__name__)

# Type alias for memory items
MemoryItem = Union[
    EpisodicEvent,
    SemanticMemoryItem,
    ProceduralMemoryItem,
    ResourceMemoryItem,
    KnowledgeVaultItem,
]


class TemporalReasoningService:
    """
    Service for temporal reasoning and memory decay modeling.

    Implements:
    - Hybrid decay function (exponential + power law based on importance)
    - Memory rehearsal (strengthening frequently/highly relevant memories)
    - Forgetting mechanisms (identifying memories for deletion)
    - Temporal scoring for retrieval ranking
    """

    def __init__(self, config=None):
        """
        Initialize the temporal reasoning service.

        Args:
            config: Optional configuration object. Defaults to temporal_settings.
        """
        self.config = config or temporal_settings

    def calculate_age_in_days(
        self, memory: MemoryItem, current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate the age of a memory in days.

        Args:
            memory: The memory item
            current_time: Current timestamp (defaults to now)

        Returns:
            Age in days as a float
        """
        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # Determine creation timestamp based on memory type
        if hasattr(memory, "occurred_at"):
            # EpisodicEvent uses occurred_at
            creation_time = memory.occurred_at
        elif hasattr(memory, "created_at"):
            # SemanticMemoryItem has explicit created_at
            creation_time = memory.created_at
        else:
            # Fallback to last_modify timestamp
            if memory.last_modify and "timestamp" in memory.last_modify:
                from dateutil import parser

                creation_time = parser.isoparse(memory.last_modify["timestamp"])
            else:
                # If no timestamp available, assume very recent
                return 0.0

        # Ensure timezone awareness
        if creation_time.tzinfo is None:
            creation_time = creation_time.replace(tzinfo=timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        age_seconds = (current_time - creation_time).total_seconds()
        age_days = age_seconds / 86400.0  # Convert to days
        return max(0.0, age_days)

    def calculate_decay_factor(
        self, memory: MemoryItem, current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate the decay factor using hybrid exponential/power law approach.

        The decay factor is a combination of exponential and power law decay,
        weighted by the importance score:
        - Low importance (→0): More exponential decay (steeper forgetting)
        - High importance (→1): More power law decay (gradual long-term retention)

        Formula:
        decay_factor = (1-w) * exp(-λ * age) + w * (1 + age)^(-α)
        where w = importance_score

        Args:
            memory: The memory item
            current_time: Current timestamp (defaults to now)

        Returns:
            Decay factor between 0 and 1
        """
        age_days = self.calculate_age_in_days(memory, current_time)
        importance = memory.importance_score

        # Clamp importance to valid range
        importance = max(
            self.config.min_importance_score,
            min(self.config.max_importance_score, importance),
        )

        # Exponential decay component (fast forgetting)
        exponential_decay = math.exp(-self.config.decay_lambda * age_days)

        # Power law decay component (slow forgetting)
        power_law_decay = math.pow(1 + age_days, -self.config.decay_alpha)

        # Hybrid: weight by importance score
        # Low importance → more exponential (w≈0)
        # High importance → more power law (w≈1)
        decay_factor = (1 - importance) * exponential_decay + importance * power_law_decay

        return max(0.0, min(1.0, decay_factor))

    def calculate_recency_bonus(
        self, memory: MemoryItem, current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate a recency bonus based on last access time.

        Recently accessed memories get a boost to their score.

        Args:
            memory: The memory item
            current_time: Current timestamp (defaults to now)

        Returns:
            Recency bonus between 0 and 1
        """
        if memory.last_accessed_at is None:
            return 0.0

        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # Ensure timezone awareness
        last_access = memory.last_accessed_at
        if last_access.tzinfo is None:
            last_access = last_access.replace(tzinfo=timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        # Calculate time since last access in days
        time_since_access = (current_time - last_access).total_seconds() / 86400.0

        # Exponential decay of recency bonus (fast decay, ~7 day half-life)
        recency_bonus = math.exp(-0.1 * time_since_access)

        return max(0.0, min(1.0, recency_bonus))

    def calculate_frequency_score(self, memory: MemoryItem) -> float:
        """
        Calculate a frequency score based on access count.

        Uses logarithmic scaling to prevent unbounded growth.

        Args:
            memory: The memory item

        Returns:
            Frequency score between 0 and 1
        """
        access_count = memory.access_count
        if access_count <= 0:
            return 0.0

        # Logarithmic scaling: log2(count + 1) / 10
        # 1 access → 0.1, 3 accesses → 0.2, 7 accesses → 0.3, etc.
        frequency_score = math.log2(access_count + 1) / 10.0

        return min(1.0, frequency_score)

    def calculate_temporal_score(
        self, memory: MemoryItem, current_time: Optional[datetime] = None
    ) -> float:
        """
        Calculate the overall temporal score for a memory.

        Combines decay factor, recency bonus, and frequency score.

        Args:
            memory: The memory item
            current_time: Current timestamp (defaults to now)

        Returns:
            Temporal score between 0 and 1
        """
        if not self.config.enabled:
            return 1.0  # If temporal reasoning disabled, return max score

        # Base decay
        decay_factor = self.calculate_decay_factor(memory, current_time)

        # Recency bonus (recently accessed memories are boosted)
        recency_bonus = self.calculate_recency_bonus(memory, current_time)

        # Frequency score (frequently accessed memories are boosted)
        frequency_score = self.calculate_frequency_score(memory)

        # Combine scores:
        # - decay_factor: base temporal decay
        # - recency_bonus: boost for recent access (up to +0.3)
        # - frequency_score: boost for frequent access (up to +0.2)
        temporal_score = decay_factor + 0.3 * recency_bonus + 0.2 * frequency_score

        return max(0.0, min(1.0, temporal_score))

    def combine_scores(
        self, relevance_score: float, temporal_score: float
    ) -> float:
        """
        Combine relevance score (BM25/embedding) with temporal score.

        Uses weighted sum based on configuration.

        Args:
            relevance_score: Relevance score from BM25 or embedding search
            temporal_score: Temporal score from calculate_temporal_score

        Returns:
            Combined final score
        """
        if not self.config.enabled:
            return relevance_score

        w_relevance = self.config.retrieval_weight_relevance
        w_temporal = self.config.retrieval_weight_temporal

        # Normalize relevance score to 0-1 range (assuming BM25 scores are typically 0-10)
        normalized_relevance = min(1.0, relevance_score / 10.0)

        combined = w_relevance * normalized_relevance + w_temporal * temporal_score

        return combined

    def should_rehearse(
        self, memory: MemoryItem, relevance_score: float
    ) -> bool:
        """
        Determine if a memory should be rehearsed (strengthened).

        Memories are rehearsed when they are retrieved with high relevance.

        Args:
            memory: The memory item
            relevance_score: Relevance score from retrieval (0-1 normalized)

        Returns:
            True if memory should be rehearsed
        """
        if not self.config.enabled:
            return False

        # Normalize relevance score if needed
        normalized_relevance = min(1.0, relevance_score / 10.0)

        return normalized_relevance >= self.config.rehearsal_threshold

    def rehearse_memory(
        self, memory: MemoryItem, session: Session
    ) -> None:
        """
        Rehearse (strengthen) a memory by updating its importance and counts.

        Args:
            memory: The memory item to rehearse
            session: Database session for committing changes
        """
        if not self.config.enabled:
            return

        # Increment rehearsal count
        memory.rehearsal_count += 1

        # Boost importance score
        new_importance = memory.importance_score + self.config.rehearsal_boost
        memory.importance_score = min(
            self.config.max_importance_score, new_importance
        )

        # Update last modified timestamp
        memory.last_modify = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": "rehearsed",
        }

        session.add(memory)
        # Note: Caller is responsible for committing the session

        logger.debug(
            f"Rehearsed memory {memory.id}: rehearsal_count={memory.rehearsal_count}, "
            f"importance_score={memory.importance_score:.3f}"
        )

    def track_access(
        self, memory: MemoryItem, session: Session
    ) -> None:
        """
        Track an access to a memory (increment access count, update timestamp).

        Args:
            memory: The memory item being accessed
            session: Database session for committing changes
        """
        if not self.config.enabled:
            return

        # Increment access count
        memory.access_count += 1

        # Update last accessed timestamp
        memory.last_accessed_at = datetime.now(timezone.utc)

        session.add(memory)
        # Note: Caller is responsible for committing the session

        logger.debug(
            f"Tracked access to memory {memory.id}: access_count={memory.access_count}"
        )

    def should_delete(
        self, memory: MemoryItem, current_time: Optional[datetime] = None
    ) -> Tuple[bool, str]:
        """
        Determine if a memory should be deleted based on temporal criteria.

        Args:
            memory: The memory item
            current_time: Current timestamp (defaults to now)

        Returns:
            Tuple of (should_delete: bool, reason: str)
        """
        if not self.config.enabled:
            return False, ""

        # Check age threshold
        age_days = self.calculate_age_in_days(memory, current_time)
        if age_days > self.config.max_age_days:
            return True, f"Exceeded max age of {self.config.max_age_days} days"

        # Check temporal score threshold
        temporal_score = self.calculate_temporal_score(memory, current_time)
        if temporal_score < self.config.deletion_threshold:
            return True, f"Temporal score {temporal_score:.3f} below threshold {self.config.deletion_threshold}"

        return False, ""

    def identify_forgettable_memories(
        self,
        session: Session,
        memory_type: type,
        organization_id: str,
        user_id: Optional[str] = None,
        current_time: Optional[datetime] = None,
        limit: int = 100,
    ) -> List[Tuple[MemoryItem, str]]:
        """
        Identify memories that should be deleted based on temporal criteria.

        Args:
            session: Database session
            memory_type: ORM class for memory type (e.g., EpisodicEvent)
            organization_id: Organization ID to filter by
            user_id: Optional user ID to filter by
            current_time: Current timestamp (defaults to now)
            limit: Maximum number of memories to return

        Returns:
            List of tuples: (memory_item, deletion_reason)
        """
        if not self.config.enabled:
            return []

        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # Build query
        query = session.query(memory_type).filter(
            memory_type.organization_id == organization_id
        )

        if user_id:
            query = query.filter(memory_type.user_id == user_id)

        # Fetch all memories (could be optimized with temporal score calculation in SQL)
        memories = query.all()

        forgettable = []
        for memory in memories:
            should_delete, reason = self.should_delete(memory, current_time)
            if should_delete:
                forgettable.append((memory, reason))

            if len(forgettable) >= limit:
                break

        logger.info(
            f"Identified {len(forgettable)} forgettable memories of type {memory_type.__name__}"
        )

        return forgettable

    def delete_forgettable_memories(
        self,
        session: Session,
        forgettable_memories: List[Tuple[MemoryItem, str]],
    ) -> int:
        """
        Delete a list of forgettable memories.

        Args:
            session: Database session
            forgettable_memories: List of (memory, reason) tuples

        Returns:
            Number of memories deleted
        """
        if not self.config.enabled:
            return 0

        deleted_count = 0
        for memory, reason in forgettable_memories:
            logger.info(f"Deleting memory {memory.id}: {reason}")
            session.delete(memory)
            deleted_count += 1

        # Commit happens outside this function
        return deleted_count


# Singleton instance
temporal_service = TemporalReasoningService()

