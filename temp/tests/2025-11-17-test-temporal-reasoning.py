"""
Comprehensive Tests for Temporal Reasoning and Memory Decay

This test suite covers:
- Hybrid decay calculations (exponential + power law)
- Memory rehearsal mechanisms
- Access tracking
- Forgetting/deletion logic
- Temporal score integration with retrieval
"""

import unittest
from datetime import datetime, timedelta, timezone
from unittest.mock import MagicMock, patch

# Mock the database context before importing services
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))


class MockMemory:
    """Mock memory object for testing"""

    def __init__(
        self,
        id="test-id",
        occurred_at=None,
        created_at=None,
        last_modify=None,
        access_count=0,
        last_accessed_at=None,
        importance_score=0.5,
        rehearsal_count=0,
    ):
        self.id = id
        self.occurred_at = occurred_at or datetime.now(timezone.utc)
        self.created_at = created_at
        self.last_modify = last_modify or {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": "created",
        }
        self.access_count = access_count
        self.last_accessed_at = last_accessed_at
        self.importance_score = importance_score
        self.rehearsal_count = rehearsal_count


class TestTemporalReasoningService(unittest.TestCase):
    """Test suite for TemporalReasoningService"""

    def setUp(self):
        """Set up test fixtures"""
        from mirix.services.temporal_reasoning_service import TemporalReasoningService
        from mirix.settings import TemporalReasoningSettings

        # Create a custom config for testing
        self.config = TemporalReasoningSettings(
            enabled=True,
            rehearsal_threshold=0.7,
            deletion_threshold=0.1,
            decay_lambda=0.05,
            decay_alpha=1.5,
            max_age_days=365,
            retrieval_weight_relevance=0.6,
            retrieval_weight_temporal=0.4,
            rehearsal_boost=0.05,
            max_importance_score=1.0,
            min_importance_score=0.0,
        )

        self.service = TemporalReasoningService(config=self.config)
        self.current_time = datetime.now(timezone.utc)

    def test_calculate_age_in_days(self):
        """Test age calculation for memories"""
        # Create a memory that's 10 days old
        old_time = self.current_time - timedelta(days=10)
        memory = MockMemory(occurred_at=old_time)

        age = self.service.calculate_age_in_days(memory, self.current_time)
        self.assertAlmostEqual(age, 10.0, delta=0.1)

    def test_calculate_age_new_memory(self):
        """Test age calculation for brand new memories"""
        memory = MockMemory(occurred_at=self.current_time)
        age = self.service.calculate_age_in_days(memory, self.current_time)
        self.assertAlmostEqual(age, 0.0, delta=0.01)

    def test_decay_factor_low_importance(self):
        """Test decay factor for low importance memories (more exponential)"""
        # 30-day-old memory with low importance (0.2)
        old_time = self.current_time - timedelta(days=30)
        memory = MockMemory(occurred_at=old_time, importance_score=0.2)

        decay_factor = self.service.calculate_decay_factor(memory, self.current_time)

        # Low importance should decay faster
        self.assertLess(decay_factor, 0.5)
        self.assertGreater(decay_factor, 0.0)

    def test_decay_factor_high_importance(self):
        """Test decay factor for high importance memories (more power law)"""
        # 30-day-old memory with high importance (0.9)
        old_time = self.current_time - timedelta(days=30)
        memory = MockMemory(occurred_at=old_time, importance_score=0.9)

        decay_factor = self.service.calculate_decay_factor(memory, self.current_time)

        # High importance should decay slower
        self.assertGreater(decay_factor, 0.5)

    def test_recency_bonus_recent_access(self):
        """Test recency bonus for recently accessed memories"""
        # Memory accessed 1 day ago
        recent_access = self.current_time - timedelta(days=1)
        memory = MockMemory(last_accessed_at=recent_access)

        bonus = self.service.calculate_recency_bonus(memory, self.current_time)

        # Should have a significant bonus
        self.assertGreater(bonus, 0.8)

    def test_recency_bonus_old_access(self):
        """Test recency bonus for memories accessed long ago"""
        # Memory accessed 30 days ago
        old_access = self.current_time - timedelta(days=30)
        memory = MockMemory(last_accessed_at=old_access)

        bonus = self.service.calculate_recency_bonus(memory, self.current_time)

        # Should have minimal bonus
        self.assertLess(bonus, 0.2)

    def test_recency_bonus_never_accessed(self):
        """Test recency bonus for memories never accessed"""
        memory = MockMemory(last_accessed_at=None)

        bonus = self.service.calculate_recency_bonus(memory, self.current_time)

        # Should be zero
        self.assertEqual(bonus, 0.0)

    def test_frequency_score_no_access(self):
        """Test frequency score for never accessed memories"""
        memory = MockMemory(access_count=0)

        score = self.service.calculate_frequency_score(memory)

        self.assertEqual(score, 0.0)

    def test_frequency_score_multiple_accesses(self):
        """Test frequency score increases with access count"""
        memory1 = MockMemory(access_count=1)
        memory2 = MockMemory(access_count=10)
        memory3 = MockMemory(access_count=100)

        score1 = self.service.calculate_frequency_score(memory1)
        score2 = self.service.calculate_frequency_score(memory2)
        score3 = self.service.calculate_frequency_score(memory3)

        # Scores should increase logarithmically
        self.assertLess(score1, score2)
        self.assertLess(score2, score3)

    def test_temporal_score_combination(self):
        """Test that temporal score combines decay, recency, and frequency"""
        # Create a well-used, recently accessed, important memory
        old_time = self.current_time - timedelta(days=10)
        recent_access = self.current_time - timedelta(days=1)

        memory = MockMemory(
            occurred_at=old_time,
            last_accessed_at=recent_access,
            access_count=10,
            importance_score=0.8,
        )

        temporal_score = self.service.calculate_temporal_score(
            memory, self.current_time
        )

        # Should have a high temporal score
        self.assertGreater(temporal_score, 0.7)
        self.assertLessEqual(temporal_score, 1.0)

    def test_combine_scores(self):
        """Test combining relevance and temporal scores"""
        relevance_score = 8.0  # BM25 score
        temporal_score = 0.8

        combined = self.service.combine_scores(relevance_score, temporal_score)

        # Should be weighted combination
        # (0.6 * 0.8) + (0.4 * 0.8) = 0.48 + 0.32 = 0.8
        self.assertAlmostEqual(combined, 0.8, delta=0.01)

    def test_should_rehearse_high_relevance(self):
        """Test rehearsal decision for high relevance retrieval"""
        memory = MockMemory()
        relevance_score = 9.0  # High BM25 score

        should_rehearse = self.service.should_rehearse(memory, relevance_score)

        # High relevance should trigger rehearsal
        self.assertTrue(should_rehearse)

    def test_should_rehearse_low_relevance(self):
        """Test rehearsal decision for low relevance retrieval"""
        memory = MockMemory()
        relevance_score = 3.0  # Low BM25 score

        should_rehearse = self.service.should_rehearse(memory, relevance_score)

        # Low relevance should not trigger rehearsal
        self.assertFalse(should_rehearse)

    def test_rehearse_memory_increases_importance(self):
        """Test that rehearsal increases importance score"""
        memory = MockMemory(importance_score=0.5, rehearsal_count=0)
        session = MagicMock()

        initial_importance = memory.importance_score
        self.service.rehearse_memory(memory, session)

        # Importance should increase by rehearsal_boost (0.05)
        self.assertAlmostEqual(
            memory.importance_score, initial_importance + 0.05, delta=0.001
        )
        self.assertEqual(memory.rehearsal_count, 1)

    def test_rehearse_memory_respects_max_importance(self):
        """Test that rehearsal doesn't exceed max importance"""
        memory = MockMemory(importance_score=0.98, rehearsal_count=5)
        session = MagicMock()

        self.service.rehearse_memory(memory, session)

        # Should be capped at max (1.0)
        self.assertLessEqual(memory.importance_score, 1.0)

    def test_track_access_increments_count(self):
        """Test that tracking access increments count and updates timestamp"""
        memory = MockMemory(access_count=0, last_accessed_at=None)
        session = MagicMock()

        self.service.track_access(memory, session)

        self.assertEqual(memory.access_count, 1)
        self.assertIsNotNone(memory.last_accessed_at)

    def test_should_delete_old_memory(self):
        """Test deletion decision for very old memories"""
        # Memory older than max_age_days (365)
        very_old_time = self.current_time - timedelta(days=400)
        memory = MockMemory(occurred_at=very_old_time)

        should_delete, reason = self.service.should_delete(memory, self.current_time)

        self.assertTrue(should_delete)
        self.assertIn("max age", reason.lower())

    def test_should_delete_low_temporal_score(self):
        """Test deletion decision for low temporal score"""
        # Old memory with low importance and no recent access
        old_time = self.current_time - timedelta(days=100)
        memory = MockMemory(
            occurred_at=old_time,
            importance_score=0.1,
            last_accessed_at=None,
            access_count=0,
        )

        should_delete, reason = self.service.should_delete(memory, self.current_time)

        # Should be marked for deletion due to low temporal score
        self.assertTrue(should_delete)

    def test_should_not_delete_important_memory(self):
        """Test that important, frequently accessed memories aren't deleted"""
        old_time = self.current_time - timedelta(days=100)
        recent_access = self.current_time - timedelta(days=1)

        memory = MockMemory(
            occurred_at=old_time,
            importance_score=0.9,
            last_accessed_at=recent_access,
            access_count=50,
        )

        should_delete, reason = self.service.should_delete(memory, self.current_time)

        # Important, well-used memory should be kept
        self.assertFalse(should_delete)

    def test_temporal_reasoning_disabled(self):
        """Test that service respects enabled flag"""
        # Create service with disabled config
        disabled_config = TemporalReasoningSettings(enabled=False)
        disabled_service = TemporalReasoningService(config=disabled_config)

        memory = MockMemory()
        session = MagicMock()

        # Should return max score when disabled
        temporal_score = disabled_service.calculate_temporal_score(
            memory, self.current_time
        )
        self.assertEqual(temporal_score, 1.0)

        # Should not rehearse when disabled
        should_rehearse = disabled_service.should_rehearse(memory, 10.0)
        self.assertFalse(should_rehearse)

        # Should not track access when disabled
        initial_count = memory.access_count
        disabled_service.track_access(memory, session)
        self.assertEqual(memory.access_count, initial_count)


class TestMemoryDecayIntegration(unittest.TestCase):
    """Integration tests for memory decay task"""

    def setUp(self):
        """Set up test fixtures"""
        from mirix.services.memory_decay_task import MemoryDecayTask

        self.decay_task = MemoryDecayTask()

    def test_decay_task_initialization(self):
        """Test that decay task initializes correctly"""
        self.assertIsNotNone(self.decay_task)
        self.assertIsNotNone(self.decay_task.logger)

    @patch("mirix.services.temporal_reasoning_service.temporal_service")
    def test_run_decay_cycle_dry_run(self, mock_service):
        """Test decay cycle in dry run mode"""
        # Mock the identify_forgettable_memories method
        mock_memory = MockMemory(id="test-1")
        mock_service.identify_forgettable_memories.return_value = [
            (mock_memory, "Low temporal score")
        ]

        session = MagicMock()
        stats = self.decay_task.run_decay_cycle(
            session=session,
            organization_id="test-org",
            user_id="test-user",
            dry_run=True,
        )

        # Should identify memories but not delete
        self.assertGreater(len(stats), 0)
        mock_service.delete_forgettable_memories.assert_not_called()


class TestTemporalScoreCalculations(unittest.TestCase):
    """Additional tests for score calculation edge cases"""

    def setUp(self):
        """Set up test fixtures"""
        from mirix.services.temporal_reasoning_service import TemporalReasoningService

        self.service = TemporalReasoningService()
        self.current_time = datetime.now(timezone.utc)

    def test_zero_age_memory(self):
        """Test calculations for brand new memories"""
        memory = MockMemory(occurred_at=self.current_time)

        decay_factor = self.service.calculate_decay_factor(memory, self.current_time)

        # Zero age should give decay factor of 1.0
        self.assertAlmostEqual(decay_factor, 1.0, delta=0.01)

    def test_importance_score_bounds(self):
        """Test that importance scores are properly bounded"""
        # Test minimum bound
        memory_min = MockMemory(importance_score=-0.5)  # Invalid negative
        decay_min = self.service.calculate_decay_factor(memory_min, self.current_time)
        self.assertGreaterEqual(decay_min, 0.0)

        # Test maximum bound
        memory_max = MockMemory(importance_score=1.5)  # Invalid over max
        decay_max = self.service.calculate_decay_factor(memory_max, self.current_time)
        self.assertLessEqual(decay_max, 1.0)


def run_tests():
    """Run all tests"""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestTemporalReasoningService))
    suite.addTests(loader.loadTestsFromTestCase(TestMemoryDecayIntegration))
    suite.addTests(loader.loadTestsFromTestCase(TestTemporalScoreCalculations))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == "__main__":
    print("=" * 70)
    print("Temporal Reasoning and Memory Decay Test Suite")
    print("=" * 70)
    print()

    success = run_tests()

    print()
    print("=" * 70)
    if success:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Please review the output above.")
    print("=" * 70)

    sys.exit(0 if success else 1)

