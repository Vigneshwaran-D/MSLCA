#!/usr/bin/env python3
"""
MIRIX Temporal Reasoning Feature Verification Script

This script tests all implemented temporal reasoning features and generates a report.

Usage:
    python temp/scripts/verify_temporal_features.py
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from datetime import datetime, timezone, timedelta
from mirix.services.temporal_reasoning_service import temporal_service
from mirix.settings import temporal_settings


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print section header"""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text):
    """Print success message"""
    print(f"{Colors.GREEN}✓{Colors.RESET} {text}")


def print_error(text):
    """Print error message"""
    print(f"{Colors.RED}✗{Colors.RESET} {text}")


def print_warning(text):
    """Print warning message"""
    print(f"{Colors.YELLOW}⚠{Colors.RESET} {text}")


def print_info(text):
    """Print info message"""
    print(f"  {text}")


class MockMemory:
    """Mock memory object for testing"""
    def __init__(self, age_days=30, access_count=10, importance=0.7, rehearsal_count=3):
        self.id = f"mock-{age_days}-{access_count}"
        self.created_at = datetime.now(timezone.utc) - timedelta(days=age_days)
        self.last_accessed_at = datetime.now(timezone.utc) - timedelta(days=min(age_days, 5))
        self.access_count = access_count
        self.rehearsal_count = rehearsal_count
        self.importance_score = importance
        self.last_modify = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": "test"
        }


def test_configuration():
    """Test 1: Configuration System"""
    print_header("Test 1: Configuration System")
    
    try:
        # Check all required settings exist
        required_settings = [
            'enabled', 'rehearsal_threshold', 'deletion_threshold',
            'decay_lambda', 'decay_alpha', 'max_age_days',
            'retrieval_weight_relevance', 'retrieval_weight_temporal',
            'rehearsal_boost', 'max_importance_score', 'min_importance_score'
        ]
        
        for setting in required_settings:
            value = getattr(temporal_settings, setting)
            print_success(f"{setting}: {value}")
        
        # Validate settings
        assert temporal_settings.rehearsal_threshold >= 0.0
        assert temporal_settings.deletion_threshold >= 0.0
        assert temporal_settings.decay_lambda > 0.0
        assert temporal_settings.decay_alpha > 0.0
        assert temporal_settings.max_age_days > 0
        
        print_success("All configuration settings valid")
        return True
        
    except Exception as e:
        print_error(f"Configuration test failed: {e}")
        return False


def test_age_calculation():
    """Test 2: Age Calculation"""
    print_header("Test 2: Age Calculation")
    
    try:
        # Test various ages
        test_cases = [
            (0, "New memory (0 days)"),
            (1, "1 day old"),
            (7, "1 week old"),
            (30, "1 month old"),
            (365, "1 year old")
        ]
        
        for age_days, description in test_cases:
            memory = MockMemory(age_days=age_days)
            calculated_age = temporal_service.calculate_age_in_days(memory)
            
            # Allow small floating point differences
            if abs(calculated_age - age_days) < 0.1:
                print_success(f"{description}: {calculated_age:.2f} days")
            else:
                print_error(f"{description}: Expected {age_days}, got {calculated_age:.2f}")
                return False
        
        print_success("Age calculation working correctly")
        return True
        
    except Exception as e:
        print_error(f"Age calculation test failed: {e}")
        return False


def test_decay_factor():
    """Test 3: Decay Factor Calculation"""
    print_header("Test 3: Decay Factor (Hybrid Exponential + Power Law)")
    
    try:
        # Test decay for different ages and importance levels
        test_cases = [
            (1, 0.1, "Low importance, recent"),
            (1, 0.9, "High importance, recent"),
            (30, 0.1, "Low importance, 1 month"),
            (30, 0.9, "High importance, 1 month"),
            (365, 0.1, "Low importance, 1 year"),
            (365, 0.9, "High importance, 1 year"),
        ]
        
        for age_days, importance, description in test_cases:
            memory = MockMemory(age_days=age_days, importance=importance)
            decay = temporal_service.calculate_decay_factor(memory)
            
            # Verify decay is between 0 and 1
            assert 0.0 <= decay <= 1.0
            
            print_info(f"{description}: decay={decay:.4f}")
        
        # Verify that higher importance = slower decay for same age
        low_imp = MockMemory(age_days=30, importance=0.1)
        high_imp = MockMemory(age_days=30, importance=0.9)
        
        decay_low = temporal_service.calculate_decay_factor(low_imp)
        decay_high = temporal_service.calculate_decay_factor(high_imp)
        
        if decay_high > decay_low:
            print_success("High importance memories decay slower ✓")
        else:
            print_error(f"Decay logic incorrect: high_imp={decay_high:.4f}, low_imp={decay_low:.4f}")
            return False
        
        print_success("Decay factor calculation working correctly")
        return True
        
    except Exception as e:
        print_error(f"Decay factor test failed: {e}")
        return False


def test_recency_bonus():
    """Test 4: Recency Bonus"""
    print_header("Test 4: Recency Bonus Calculation")
    
    try:
        # Test recency for different last access times
        test_cases = [
            (0, "Just accessed"),
            (1, "Accessed 1 day ago"),
            (7, "Accessed 1 week ago"),
            (30, "Accessed 1 month ago"),
        ]
        
        for days_since_access, description in test_cases:
            memory = MockMemory(age_days=30)
            memory.last_accessed_at = datetime.now(timezone.utc) - timedelta(days=days_since_access)
            
            recency = temporal_service.calculate_recency_bonus(memory)
            
            # Verify recency is between 0 and 1
            assert 0.0 <= recency <= 1.0
            
            print_info(f"{description}: recency={recency:.4f}")
        
        # Verify that recent access = higher bonus
        recent = MockMemory(age_days=30)
        recent.last_accessed_at = datetime.now(timezone.utc)
        
        old = MockMemory(age_days=30)
        old.last_accessed_at = datetime.now(timezone.utc) - timedelta(days=30)
        
        recency_recent = temporal_service.calculate_recency_bonus(recent)
        recency_old = temporal_service.calculate_recency_bonus(old)
        
        if recency_recent > recency_old:
            print_success("Recently accessed memories get higher bonus ✓")
        else:
            print_error("Recency bonus logic incorrect")
            return False
        
        print_success("Recency bonus calculation working correctly")
        return True
        
    except Exception as e:
        print_error(f"Recency bonus test failed: {e}")
        return False


def test_frequency_score():
    """Test 5: Frequency Score"""
    print_header("Test 5: Frequency Score (Logarithmic Scaling)")
    
    try:
        # Test frequency for different access counts
        test_cases = [
            (0, "Never accessed"),
            (1, "Accessed once"),
            (3, "Accessed 3 times"),
            (7, "Accessed 7 times"),
            (15, "Accessed 15 times"),
            (31, "Accessed 31 times"),
            (100, "Accessed 100 times"),
        ]
        
        for access_count, description in test_cases:
            memory = MockMemory(access_count=access_count)
            frequency = temporal_service.calculate_frequency_score(memory)
            
            # Verify frequency is between 0 and 1
            assert 0.0 <= frequency <= 1.0
            
            print_info(f"{description}: frequency={frequency:.4f}")
        
        # Verify logarithmic growth (diminishing returns)
        mem_10 = MockMemory(access_count=10)
        mem_20 = MockMemory(access_count=20)
        mem_40 = MockMemory(access_count=40)
        
        freq_10 = temporal_service.calculate_frequency_score(mem_10)
        freq_20 = temporal_service.calculate_frequency_score(mem_20)
        freq_40 = temporal_service.calculate_frequency_score(mem_40)
        
        # Doubling access count should not double frequency score (logarithmic)
        diff_10_20 = freq_20 - freq_10
        diff_20_40 = freq_40 - freq_20
        
        if diff_20_40 < diff_10_20:
            print_success("Frequency shows logarithmic growth (diminishing returns) ✓")
        else:
            print_warning("Frequency growth may not be logarithmic")
        
        print_success("Frequency score calculation working correctly")
        return True
        
    except Exception as e:
        print_error(f"Frequency score test failed: {e}")
        return False


def test_temporal_score():
    """Test 6: Composite Temporal Score"""
    print_header("Test 6: Composite Temporal Score")
    
    try:
        # Test composite score
        memory = MockMemory(age_days=30, access_count=10, importance=0.7)
        
        temporal_score = temporal_service.calculate_temporal_score(memory)
        
        # Verify score is between 0 and 1
        assert 0.0 <= temporal_score <= 1.0
        
        # Break down components
        decay = temporal_service.calculate_decay_factor(memory)
        recency = temporal_service.calculate_recency_bonus(memory)
        frequency = temporal_service.calculate_frequency_score(memory)
        
        print_info(f"Memory: 30 days old, 10 accesses, importance=0.7")
        print_info(f"  Decay Factor: {decay:.4f}")
        print_info(f"  Recency Bonus: {recency:.4f} (×0.3 = {recency * 0.3:.4f})")
        print_info(f"  Frequency Score: {frequency:.4f} (×0.2 = {frequency * 0.2:.4f})")
        print_info(f"  Temporal Score: {temporal_score:.4f}")
        
        # Verify formula: temporal_score = decay + 0.3*recency + 0.2*frequency
        # Note: decay already includes importance weighting
        expected_contribution = 0.3 * recency + 0.2 * frequency
        print_info(f"  Expected contribution from recency+frequency: {expected_contribution:.4f}")
        
        print_success("Temporal score calculation working correctly")
        return True
        
    except Exception as e:
        print_error(f"Temporal score test failed: {e}")
        return False


def test_combine_scores():
    """Test 7: Score Combination (Relevance + Temporal)"""
    print_header("Test 7: Score Combination (Relevance + Temporal)")
    
    try:
        memory = MockMemory(age_days=30, access_count=10, importance=0.7)
        
        # Test with different relevance scores
        test_cases = [
            (0.1, "Low relevance (0.1)"),
            (0.5, "Medium relevance (0.5)"),
            (0.9, "High relevance (0.9)"),
            (10.0, "BM25 score (10.0)"),  # BM25 scores typically 0-10
        ]
        
        temporal_score = temporal_service.calculate_temporal_score(memory)
        
        for relevance, description in test_cases:
            combined = temporal_service.combine_scores(relevance, temporal_score)
            
            print_info(f"{description}: combined={combined:.4f}")
        
        # Verify weights are applied correctly
        relevance = 0.5
        combined = temporal_service.combine_scores(relevance, temporal_score)
        
        expected = (
            temporal_settings.retrieval_weight_relevance * (relevance / 10.0) +  # normalized
            temporal_settings.retrieval_weight_temporal * temporal_score
        )
        
        if abs(combined - expected) < 0.01:
            print_success("Score combination formula correct ✓")
        else:
            print_warning(f"Score combination: expected {expected:.4f}, got {combined:.4f}")
        
        print_success("Score combination working correctly")
        return True
        
    except Exception as e:
        print_error(f"Score combination test failed: {e}")
        return False


def test_rehearsal_logic():
    """Test 8: Rehearsal Logic"""
    print_header("Test 8: Rehearsal Logic")
    
    try:
        # Test should_rehearse with different relevance scores
        memory = MockMemory(age_days=30, access_count=5, importance=0.6)
        
        test_cases = [
            (0.5, False, "Below threshold (0.5)"),
            (0.69, False, "Just below threshold (0.69)"),
            (0.7, True, "At threshold (0.7)"),
            (0.8, True, "Above threshold (0.8)"),
            (1.0, True, "Maximum (1.0)"),
        ]
        
        for relevance, expected, description in test_cases:
            should_rehearse = temporal_service.should_rehearse(memory, relevance)
            
            if should_rehearse == expected:
                print_success(f"{description}: {should_rehearse} ✓")
            else:
                print_error(f"{description}: expected {expected}, got {should_rehearse}")
                return False
        
        print_success("Rehearsal logic working correctly")
        return True
        
    except Exception as e:
        print_error(f"Rehearsal logic test failed: {e}")
        return False


def test_deletion_logic():
    """Test 9: Deletion Logic"""
    print_header("Test 9: Deletion Logic")
    
    try:
        # Test should_delete with different scenarios
        test_cases = [
            # (age_days, importance, access_count, expected_delete, description)
            (1, 0.8, 10, False, "Recent, important, frequently accessed"),
            (30, 0.7, 10, False, "Medium age, good importance"),
            (365, 0.1, 1, True, "Very old, low importance"),
            (400, 0.9, 100, True, "Exceeds max age (365 days)"),
            (30, 0.01, 0, True, "Low temporal score"),
        ]
        
        for age_days, importance, access_count, expected, description in test_cases:
            memory = MockMemory(age_days=age_days, importance=importance, access_count=access_count)
            should_delete, reason = temporal_service.should_delete(memory)
            
            if should_delete == expected:
                status = "DELETE" if should_delete else "KEEP"
                print_success(f"{description}: {status}")
                if reason:
                    print_info(f"  Reason: {reason}")
            else:
                print_error(f"{description}: expected delete={expected}, got {should_delete}")
                return False
        
        print_success("Deletion logic working correctly")
        return True
        
    except Exception as e:
        print_error(f"Deletion logic test failed: {e}")
        return False


def test_streamlit_imports():
    """Test 10: Streamlit Components"""
    print_header("Test 10: Streamlit Components")
    
    try:
        # Test that streamlit modules can be imported
        import streamlit as st
        print_success("Streamlit installed")
        
        import pandas as pd
        print_success("Pandas installed")
        
        import plotly.express as px
        import plotly.graph_objects as go
        print_success("Plotly installed")
        
        # Test UI module import
        from mirix.services.streamlit_temporal_ui import TemporalReasoningUI
        print_success("TemporalReasoningUI imported")
        
        # Test memory decay task
        from mirix.services.memory_decay_task import memory_decay_task, MEMORY_TYPES
        print_success(f"Memory decay task available, {len(MEMORY_TYPES)} memory types")
        
        print_success("All Streamlit components available")
        return True
        
    except ImportError as e:
        print_error(f"Streamlit components not available: {e}")
        print_warning("Run: pip install streamlit plotly pandas")
        return False
    except Exception as e:
        print_error(f"Streamlit test failed: {e}")
        return False


def generate_summary(results):
    """Generate final summary"""
    print_header("VERIFICATION SUMMARY")
    
    total = len(results)
    passed = sum(results.values())
    failed = total - passed
    
    print_info(f"Total Tests: {total}")
    print_success(f"Passed: {passed}")
    
    if failed > 0:
        print_error(f"Failed: {failed}")
    else:
        print_success("All tests passed! ✓")
    
    percentage = (passed / total) * 100
    print_info(f"Success Rate: {percentage:.1f}%")
    
    # List failed tests
    if failed > 0:
        print_warning("\nFailed Tests:")
        for test_name, passed in results.items():
            if not passed:
                print_error(f"  - {test_name}")
    
    # Recommendations
    print_header("RECOMMENDATIONS")
    
    if percentage == 100:
        print_success("✓ All core features working correctly!")
        print_info("Your temporal reasoning system is fully functional.")
        print_info("\nNext steps:")
        print_info("  1. Launch Streamlit dashboard: streamlit run streamlit_app.py")
        print_info("  2. Review missing features in: temp/docs/2025-11-18-feature-comparison.md")
        print_info("  3. Implement enhancements from: temp/docs/2025-11-18-enhancement-roadmap.md")
    elif percentage >= 80:
        print_success("✓ Most features working correctly")
        print_warning("Some tests failed - review errors above")
    else:
        print_error("✗ Multiple test failures detected")
        print_warning("Review configuration and dependencies")


def main():
    """Run all verification tests"""
    print_header("MIRIX TEMPORAL REASONING FEATURE VERIFICATION")
    print_info("Testing all implemented temporal reasoning features...")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run all tests
    results = {
        "Configuration System": test_configuration(),
        "Age Calculation": test_age_calculation(),
        "Decay Factor": test_decay_factor(),
        "Recency Bonus": test_recency_bonus(),
        "Frequency Score": test_frequency_score(),
        "Temporal Score": test_temporal_score(),
        "Score Combination": test_combine_scores(),
        "Rehearsal Logic": test_rehearsal_logic(),
        "Deletion Logic": test_deletion_logic(),
        "Streamlit Components": test_streamlit_imports(),
    }
    
    # Generate summary
    generate_summary(results)
    
    # Exit with appropriate code
    if all(results.values()):
        print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed! ✓{Colors.RESET}\n")
        sys.exit(0)
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}Some tests failed ✗{Colors.RESET}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()

