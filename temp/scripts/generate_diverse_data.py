#!/usr/bin/env python3
"""
Generate Diverse Test Data for Status Visualization

Creates data with:
- Green status: High importance (≥0.7)
- Red status: Forgettable (very old or low importance)
- White status: Normal retention
"""

import sys
import uuid
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mirix.server.server import db_context
from mirix.orm.episodic_memory import EpisodicEvent
from mirix.orm.chat_message import ChatMessage

print("\n" + "="*70)
print("Diverse Test Data Generator")
print("Creating data with all status types: Green, Red, and White")
print("="*70)

ORG_ID = "1234"
USER_ID = "user-d1850539"

now = datetime.now(timezone.utc)

# Sample content
EVENTS = [
    "Critical system deployment",
    "Important client meeting",
    "Regular code review",
    "Minor bug fix",
    "Documentation update",
    "Old archived task",
    "Deprecated feature cleanup",
    "Obsolete reference material"
]

try:
    with db_context() as session:
        print("\n[1/4] Creating HIGH IMPORTANCE Events (Green Status)...")
        print("  - Importance >= 0.7")
        print("  - Recent (0-30 days)")
        print("  - Frequently accessed")
        
        for i in range(10):
            memory = EpisodicEvent(
                id=f"ep-high-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                actor="system",
                event_type="critical",
                occurred_at=now - timedelta(days=random.randint(0, 30)),
                summary=f"High Priority: {EVENTS[0]}",
                details=f"Critical event {i+1} - High importance, well-maintained",
                importance_score=random.uniform(0.75, 0.95),  # High importance
                access_count=random.randint(10, 30),  # Frequently accessed
                last_accessed_at=now - timedelta(days=random.randint(0, 5)),
                rehearsal_count=random.randint(5, 15),
            )
            session.add(memory)
        session.commit()
        print("  [OK] Created 10 high importance events (will show GREEN)")
        
        print("\n[2/4] Creating FORGETTABLE Events (Red Status)...")
        print("  - Very old (>365 days) OR")
        print("  - Low importance (<0.2) with age >90 days")
        
        # Very old events (>365 days)
        for i in range(8):
            memory = EpisodicEvent(
                id=f"ep-old-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                actor="system",
                event_type="archived",
                occurred_at=now - timedelta(days=random.randint(370, 450)),  # Very old
                summary=f"Old Archived: {EVENTS[5]}",
                details=f"Old event {i+1} - Exceeds max age (365 days)",
                importance_score=random.uniform(0.1, 0.4),  # Low importance
                access_count=random.randint(0, 2),  # Rarely accessed
                last_accessed_at=None,  # Never accessed recently
                rehearsal_count=0,
            )
            session.add(memory)
        
        # Low importance, moderately old
        for i in range(7):
            memory = EpisodicEvent(
                id=f"ep-lowp-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                actor="system",
                event_type="deprecated",
                occurred_at=now - timedelta(days=random.randint(100, 200)),
                summary=f"Low Priority: {EVENTS[6]}",
                details=f"Low importance event {i+1} - Temporal score too low",
                importance_score=random.uniform(0.05, 0.15),  # Very low importance
                access_count=random.randint(0, 1),
                last_accessed_at=None,
                rehearsal_count=0,
            )
            session.add(memory)
        
        session.commit()
        print("  [OK] Created 15 forgettable events (will show RED)")
        
        print("\n[3/4] Creating NORMAL Events (White Status)...")
        print("  - Medium importance (0.4-0.7)")
        print("  - Medium age (30-180 days)")
        
        for i in range(15):
            memory = EpisodicEvent(
                id=f"ep-norm-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                actor="system",
                event_type="normal",
                occurred_at=now - timedelta(days=random.randint(30, 180)),
                summary=f"Normal: {EVENTS[2]}",
                details=f"Normal event {i+1} - Standard retention",
                importance_score=random.uniform(0.40, 0.69),  # Medium importance
                access_count=random.randint(2, 8),
                last_accessed_at=now - timedelta(days=random.randint(10, 60)),
                rehearsal_count=random.randint(1, 4),
            )
            session.add(memory)
        session.commit()
        print("  [OK] Created 15 normal events (will show WHITE)")
        
        print("\n[4/4] Creating DIVERSE Chat Messages...")
        
        session_id = f"diverse-{uuid.uuid4().hex[:8]}"
        
        # High importance chats (5)
        for i in range(5):
            memory = ChatMessage(
                id=f"msg-high-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                session_id=session_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Important question {i+1}: Critical system inquiry",
                importance_score=random.uniform(0.75, 0.9),
                access_count=random.randint(8, 20),
                last_accessed_at=now - timedelta(days=random.randint(0, 3)),
                rehearsal_count=random.randint(3, 8),
            )
            session.add(memory)
        
        # Forgettable chats (8) - very old
        for i in range(8):
            memory = ChatMessage(
                id=f"msg-old-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                session_id=session_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Old chat {i+1}: Obsolete conversation",
                importance_score=random.uniform(0.1, 0.3),
                access_count=0,
                last_accessed_at=None,
                rehearsal_count=0,
            )
            session.add(memory)
        
        # Normal chats (7)
        for i in range(7):
            memory = ChatMessage(
                id=f"msg-norm-{uuid.uuid4().hex[:20]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                session_id=session_id,
                role="user" if i % 2 == 0 else "assistant",
                content=f"Normal chat {i+1}: Regular conversation",
                importance_score=random.uniform(0.4, 0.65),
                access_count=random.randint(2, 6),
                last_accessed_at=now - timedelta(days=random.randint(5, 20)),
                rehearsal_count=random.randint(1, 3),
            )
            session.add(memory)
        
        session.commit()
        print("  [OK] Created 20 diverse chat messages")
        
        # Summary
        print("\n" + "="*70)
        print("SUCCESS! Diverse data created")
        print("="*70)
        print("\nBreakdown by Status:")
        print("\n  EPISODIC EVENTS (40 new):")
        print("    [GREEN] High Importance:  10 events")
        print("    [RED] Forgettable:        15 events")
        print("    [WHITE] Normal:           15 events")
        print("\n  CHAT MESSAGES (20 new):")
        print("    [GREEN] High Importance:  5 messages")
        print("    [RED] Forgettable:        8 messages")
        print("    [WHITE] Normal:           7 messages")
        
        print("\n" + "="*70)
        print("Now refresh Streamlit and go to Database View!")
        print("="*70)
        print("\nYou should now see:")
        print("  - Green rows (high importance >= 0.7)")
        print("  - Red rows (forgettable - old or low score)")
        print("  - White rows (normal retention)")
        print("\nTry the Cleanup tab to:")
        print("  - Scan for forgettable memories (~23 should be found)")
        print("  - Preview deletions in dry-run mode")
        print("  - Delete the red ones to clean up!")
        print("="*70 + "\n")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

