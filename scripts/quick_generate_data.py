#!/usr/bin/env python3
"""Quick data generator - simplified version that works"""

import sys
import uuid
import random
from pathlib import Path
from datetime import datetime, timezone, timedelta

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mirix.server.server import db_context
from mirix.orm.episodic_memory import EpisodicEvent
from mirix.orm.chat_message import ChatMessage

print("\n" + "="*60)
print("Quick Test Data Generator")
print("="*60)

# Your credentials
ORG_ID = "1234"
USER_ID = "user-d1850539"

now = datetime.now(timezone.utc)

# Sample content
EVENTS = [
    "Had a meeting", "Deployed code", "Fixed bug", 
    "Updated docs", "Reviewed PR", "Wrote tests"
]

CHAT_MSGS = [
    "How does temporal reasoning work?",
    "Show me the dashboard",
    "What's my memory usage?",
    "Explain decay functions",
    "Help with settings"
]

try:
    with db_context() as session:
        # Generate 10 more episodic events
        print(f"\n[1/2] Creating 10 more Episodic Events...")
        for i in range(10):
            days_ago = random.randint(0, 100)
            memory = EpisodicEvent(
                id=f"ep-{uuid.uuid4().hex[:24]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                actor="system",
                event_type="activity",
                occurred_at=now - timedelta(days=days_ago),
                summary=random.choice(EVENTS),
                details=f"Test event {i+1} from {days_ago} days ago",
                importance_score=random.uniform(0.3, 0.9),
                access_count=random.randint(0, 10),
                last_accessed_at=now - timedelta(days=random.randint(0, days_ago)) if random.random() > 0.3 else None,
                rehearsal_count=random.randint(0, 5),
            )
            session.add(memory)
        session.commit()
        print("   [OK] Created 10 episodic events")
        
        # Generate 25 chat messages
        print(f"\n[2/2] Creating 25 Chat Messages...")
        session_id = f"test-{uuid.uuid4().hex[:8]}"
        for i in range(25):
            days_ago = random.randint(0, 30)
            role = "user" if i % 2 == 0 else "assistant"
            
            memory = ChatMessage(
                id=f"msg-{uuid.uuid4().hex[:24]}",
                organization_id=ORG_ID,
                user_id=USER_ID,
                session_id=session_id,
                role=role,
                content=random.choice(CHAT_MSGS) if role == "user" else f"Response to: {random.choice(CHAT_MSGS)}",
                importance_score=random.uniform(0.3, 0.8),
                access_count=random.randint(0, 8),
                last_accessed_at=now - timedelta(days=random.randint(0, days_ago)) if random.random() > 0.5 else None,
                rehearsal_count=random.randint(0, 3),
            )
            session.add(memory)
        session.commit()
        print("   [OK] Created 25 chat messages")
        
        print("\n" + "="*60)
        print("SUCCESS! Data created for:")
        print(f"  Organization: {ORG_ID}")
        print(f"  User: {USER_ID}")
        print("\nTotal generated:")
        print(f"  - 10 more Episodic Events (now 40 total)")
        print(f"  - 25 Chat Messages (new!)")
        print("\n" + "="*60)
        print("\nNow refresh your Streamlit dashboard!")
        print("  - Database View → Episodic Events (40 records)")
        print("  - Database View → Chat Messages (25 records)")
        print("="*60 + "\n")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

