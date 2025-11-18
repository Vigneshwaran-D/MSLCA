#!/usr/bin/env python3
"""
MIRIX Synthetic Test Data Generator

Creates realistic test data for temporal memory system testing.
Generates memories with varying ages, importance scores, access patterns, and decay states.

Usage:
    python temp/scripts/generate_synthetic_test_data.py --org-id 1234 --user-id user-d1850539
"""

import sys
import argparse
import random
import uuid
from pathlib import Path
from datetime import datetime, timezone, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from mirix.server.server import db_context
from mirix.orm.episodic_memory import EpisodicEvent
from mirix.orm.semantic_memory import SemanticMemoryItem
from mirix.orm.procedural_memory import ProceduralMemoryItem
from mirix.orm.resource_memory import ResourceMemoryItem
from mirix.orm.knowledge_vault import KnowledgeVaultItem
from mirix.orm.chat_message import ChatMessage
from mirix.orm.organization import Organization
from mirix.orm.user import User
from mirix.log import get_logger

logger = get_logger(__name__)


class Colors:
    """ANSI color codes"""
    GREEN = '\033[92m'
    BLUE = '\033[94m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*70}{Colors.RESET}\n")


def print_success(text):
    print(f"{Colors.GREEN}[OK]{Colors.RESET} {text}")


def print_info(text):
    print(f"  {text}")


def print_warning(text):
    print(f"{Colors.YELLOW}[WARN]{Colors.RESET} {text}")


def print_error(text):
    print(f"{Colors.RED}[ERROR]{Colors.RESET} {text}")


def ensure_org_and_user_exist(session, org_id, user_id):
    """Ensure organization and user exist, create if not"""
    
    # Check/create organization
    org = session.query(Organization).filter(Organization.id == org_id).first()
    if not org:
        print_info(f"Creating organization: {org_id}")
        org = Organization(
            id=org_id,
            name=f"Test Organization {org_id}"
        )
        session.add(org)
        session.commit()
        print_success(f"Created organization: {org_id}")
    else:
        print_info(f"Organization exists: {org_id}")
    
    # Check/create user
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        print_info(f"Creating user: {user_id}")
        user = User(
            id=user_id,
            name="Test User",
            organization_id=org_id,
            timezone="UTC"
        )
        session.add(user)
        session.commit()
        print_success(f"Created user: {user_id}")
    else:
        print_info(f"User exists: {user_id}")
    
    return org, user


# Sample content for different memory types
EPISODIC_EVENTS = [
    "Had a productive meeting about the new project roadmap",
    "Discussed architecture decisions for the memory system",
    "Reviewed code changes with the team",
    "Deployed the new feature to production",
    "Fixed critical bug in the authentication module",
    "Attended workshop on machine learning",
    "Brainstormed ideas for improving user experience",
    "Collaborated on database optimization",
    "Resolved merge conflict in the main branch",
    "Conducted performance testing on the API",
    "Updated documentation for the temporal system",
    "Refactored the memory management code",
    "Investigated slow query performance",
    "Implemented new caching strategy",
    "Participated in sprint planning meeting",
    "Debugged memory leak in the background worker",
    "Set up CI/CD pipeline for automated testing",
    "Reviewed pull request for feature enhancement",
    "Analyzed user feedback and bug reports",
    "Migrated database to new schema version",
]

SEMANTIC_FACTS = [
    "Python is a high-level programming language",
    "REST APIs use HTTP methods like GET, POST, PUT, DELETE",
    "PostgreSQL supports JSONB data type for JSON storage",
    "Temporal reasoning involves time-based memory decay",
    "Exponential decay follows the formula: e^(-λt)",
    "Streamlit is a Python framework for building web apps",
    "Vector databases enable semantic search capabilities",
    "BM25 is a ranking function used in information retrieval",
    "Hybrid decay combines exponential and power law functions",
    "Memory rehearsal strengthens important memories",
    "Access frequency affects memory retention",
    "Importance score ranges from 0.0 to 1.0",
    "Recency bonus decays exponentially over time",
    "SQLAlchemy is a Python SQL toolkit and ORM",
    "Embeddings convert text to high-dimensional vectors",
]

PROCEDURAL_SKILLS = [
    "How to implement exponential decay in Python",
    "Steps to configure database connection pooling",
    "Process for deploying to production environment",
    "Workflow for code review and approval",
    "Method for calculating temporal scores",
    "Procedure for running database migrations",
    "Technique for optimizing slow SQL queries",
    "Strategy for implementing memory cleanup tasks",
    "Approach to debugging production issues",
    "Guidelines for writing effective tests",
]

RESOURCE_REFERENCES = [
    "Memory System Documentation: docs/temporal-memory.md",
    "API Specification: api/v1/memories",
    "Database Schema: schema/memories.sql",
    "Streamlit Dashboard Code: streamlit_app.py",
    "Configuration File: mirix/settings.py",
    "Test Suite: tests/test_temporal_reasoning.py",
    "Migration Script: database/add_temporal_fields.py",
    "User Guide: docs/user-guide.md",
    "Architecture Diagram: docs/architecture.png",
    "Performance Benchmarks: benchmarks/results.csv",
]

KNOWLEDGE_VAULT = [
    "Best practices for temporal memory management",
    "Understanding hybrid decay functions",
    "Memory tier classification strategies",
    "Techniques for preventing memory bloat",
    "Approaches to multi-agent coordination",
    "Methods for calculating composite scores",
    "Strategies for memory consolidation",
    "Guidelines for setting decay parameters",
    "Tips for optimizing retrieval performance",
    "Patterns for memory rehearsal scheduling",
]

CHAT_MESSAGES = [
    "What is the current status of the temporal reasoning system?",
    "Can you explain how memory decay works?",
    "How do I adjust the decay parameters?",
    "Show me memories that are about to expire",
    "What's the average importance score of my memories?",
    "Help me understand the hybrid decay function",
    "How can I improve memory retention?",
    "What factors affect temporal scores?",
    "Can you list the most frequently accessed memories?",
    "Explain the difference between recency and frequency",
    "How do I run the memory cleanup task?",
    "What does the rehearsal threshold control?",
    "Show me analytics about my memory usage",
    "How old is the oldest memory in the system?",
    "What percentage of memories are forgettable?",
]


def create_episodic_memories(session, org_id, user_id, count=30):
    """Create episodic event memories with varying ages and importance"""
    print_header(f"Creating {count} Episodic Memories")
    
    now = datetime.now(timezone.utc)
    memories = []
    
    # Create memories with different age profiles
    age_profiles = [
        # (days_ago_min, days_ago_max, importance_range, access_count_range, label)
        (0, 2, (0.7, 0.9), (5, 15), "Very Recent & Important"),
        (3, 7, (0.6, 0.8), (3, 10), "Recent & Relevant"),
        (8, 30, (0.5, 0.7), (1, 5), "Medium Age"),
        (31, 90, (0.3, 0.6), (0, 3), "Older Memories"),
        (91, 180, (0.2, 0.4), (0, 2), "Old & Fading"),
        (181, 400, (0.1, 0.3), (0, 1), "Very Old (Near Expiry)"),
    ]
    
    memories_per_profile = count // len(age_profiles)
    
    for days_min, days_max, (imp_min, imp_max), (acc_min, acc_max), label in age_profiles:
        print_info(f"Creating {label} memories...")
        
        for i in range(memories_per_profile):
            # Random age within range
            days_ago = random.randint(days_min, days_max)
            occurred_at = now - timedelta(days=days_ago)
            
            # Random importance and access count
            importance = random.uniform(imp_min, imp_max)
            access_count = random.randint(acc_min, acc_max)
            rehearsal_count = min(access_count // 3, random.randint(0, 5))
            
            # Last accessed time (within memory lifetime)
            days_since_access = min(days_ago, random.randint(0, max(1, days_ago // 2)))
            last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
            
            # Random content
            content = random.choice(EPISODIC_EVENTS)
            
            memory = EpisodicEvent(
                id=f"ep-{uuid.uuid4().hex[:24]}",
                organization_id=org_id,
                user_id=user_id,
                actor="system",
                event_type="activity",
                occurred_at=occurred_at,
                summary=content,
                details=f"{content} ({days_ago} days ago) - Synthetic test data",
                importance_score=importance,
                access_count=access_count,
                last_accessed_at=last_accessed_at,
                rehearsal_count=rehearsal_count,
                last_modify={
                    "timestamp": now.isoformat(),
                    "operation": "synthetic_data_generation"
                }
            )
            
            memories.append(memory)
            session.add(memory)
    
    session.commit()
    print_success(f"Created {len(memories)} episodic memories")
    return len(memories)


def create_semantic_memories(session, org_id, user_id, count=20):
    """Create semantic memory items (facts and concepts)"""
    print_header(f"Creating {count} Semantic Memories")
    
    now = datetime.now(timezone.utc)
    memories = []
    
    # Semantic memories tend to be longer-lived
    age_profiles = [
        (0, 7, (0.8, 0.95), (10, 30), "Core Knowledge"),
        (8, 30, (0.7, 0.85), (5, 15), "Important Facts"),
        (31, 180, (0.5, 0.7), (2, 8), "General Knowledge"),
        (181, 365, (0.3, 0.5), (0, 3), "Older Facts"),
    ]
    
    memories_per_profile = count // len(age_profiles)
    
    for days_min, days_max, (imp_min, imp_max), (acc_min, acc_max), label in age_profiles:
        print_info(f"Creating {label}...")
        
        for i in range(memories_per_profile):
            days_ago = random.randint(days_min, days_max)
            created_at = now - timedelta(days=days_ago)
            
            importance = random.uniform(imp_min, imp_max)
            access_count = random.randint(acc_min, acc_max)
            rehearsal_count = min(access_count // 2, random.randint(0, 10))
            
            days_since_access = min(days_ago, random.randint(0, max(1, days_ago // 3)))
            last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
            
            content = random.choice(SEMANTIC_FACTS)
            
            memory = SemanticMemoryItem(
                organization_id=org_id,
                user_id=user_id,
                content=content,
                concept_type="fact",
                created_at=created_at,
                importance_score=importance,
                access_count=access_count,
                last_accessed_at=last_accessed_at,
                rehearsal_count=rehearsal_count,
                last_modify={
                    "timestamp": now.isoformat(),
                    "operation": "synthetic_data_generation"
                }
            )
            
            memories.append(memory)
            session.add(memory)
    
    session.commit()
    print_success(f"Created {len(memories)} semantic memories")
    return len(memories)


def create_procedural_memories(session, org_id, user_id, count=15):
    """Create procedural memory items (skills and procedures)"""
    print_header(f"Creating {count} Procedural Memories")
    
    now = datetime.now(timezone.utc)
    memories = []
    
    # Procedural memories decay slowly but can become obsolete
    for i in range(count):
        days_ago = random.randint(0, 200)
        created_at = now - timedelta(days=days_ago)
        
        # Skills used frequently are more important
        if days_ago < 30:
            importance = random.uniform(0.7, 0.9)
            access_count = random.randint(5, 20)
        elif days_ago < 90:
            importance = random.uniform(0.5, 0.7)
            access_count = random.randint(2, 10)
        else:
            importance = random.uniform(0.3, 0.6)
            access_count = random.randint(0, 5)
        
        rehearsal_count = min(access_count // 2, random.randint(0, 8))
        
        days_since_access = min(days_ago, random.randint(0, max(1, days_ago // 2)))
        last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
        
        content = random.choice(PROCEDURAL_SKILLS)
        
        memory = ProceduralMemoryItem(
            organization_id=org_id,
            user_id=user_id,
            skill_name=content,
            description=f"Procedure: {content}",
            importance_score=importance,
            access_count=access_count,
            last_accessed_at=last_accessed_at,
            rehearsal_count=rehearsal_count,
            last_modify={
                "timestamp": created_at.isoformat(),
                "operation": "synthetic_data_generation"
            }
        )
        
        memories.append(memory)
        session.add(memory)
    
    session.commit()
    print_success(f"Created {len(memories)} procedural memories")
    return len(memories)


def create_resource_memories(session, org_id, user_id, count=10):
    """Create resource memory items (references and links)"""
    print_header(f"Creating {count} Resource Memories")
    
    now = datetime.now(timezone.utc)
    memories = []
    
    for i in range(count):
        days_ago = random.randint(0, 150)
        created_at = now - timedelta(days=days_ago)
        
        if days_ago < 30:
            importance = random.uniform(0.6, 0.8)
            access_count = random.randint(3, 15)
        else:
            importance = random.uniform(0.4, 0.6)
            access_count = random.randint(0, 5)
        
        rehearsal_count = min(access_count // 3, random.randint(0, 5))
        
        days_since_access = min(days_ago, random.randint(0, max(1, days_ago // 2)))
        last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
        
        resource = random.choice(RESOURCE_REFERENCES)
        
        memory = ResourceMemoryItem(
            organization_id=org_id,
            user_id=user_id,
            resource_name=resource,
            resource_type="documentation",
            description=f"Reference: {resource}",
            importance_score=importance,
            access_count=access_count,
            last_accessed_at=last_accessed_at,
            rehearsal_count=rehearsal_count,
            last_modify={
                "timestamp": created_at.isoformat(),
                "operation": "synthetic_data_generation"
            }
        )
        
        memories.append(memory)
        session.add(memory)
    
    session.commit()
    print_success(f"Created {len(memories)} resource memories")
    return len(memories)


def create_knowledge_vault_items(session, org_id, user_id, count=10):
    """Create knowledge vault items"""
    print_header(f"Creating {count} Knowledge Vault Items")
    
    now = datetime.now(timezone.utc)
    memories = []
    
    for i in range(count):
        days_ago = random.randint(0, 100)
        created_at = now - timedelta(days=days_ago)
        
        # Knowledge vault items tend to be important
        importance = random.uniform(0.7, 0.95)
        access_count = random.randint(2, 20)
        rehearsal_count = min(access_count // 2, random.randint(0, 10))
        
        days_since_access = min(days_ago, random.randint(0, max(1, days_ago // 3)))
        last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
        
        knowledge = random.choice(KNOWLEDGE_VAULT)
        
        memory = KnowledgeVaultItem(
            organization_id=org_id,
            user_id=user_id,
            title=knowledge,
            content=f"Knowledge: {knowledge}",
            category="best_practices",
            importance_score=importance,
            access_count=access_count,
            last_accessed_at=last_accessed_at,
            rehearsal_count=rehearsal_count,
            last_modify={
                "timestamp": created_at.isoformat(),
                "operation": "synthetic_data_generation"
            }
        )
        
        memories.append(memory)
        session.add(memory)
    
    session.commit()
    print_success(f"Created {len(memories)} knowledge vault items")
    return len(memories)


def create_chat_messages(session, org_id, user_id, count=25):
    """Create chat messages (most volatile memory type)"""
    print_header(f"Creating {count} Chat Messages")
    
    now = datetime.now(timezone.utc)
    messages = []
    
    session_id = f"test-session-{random.randint(1000, 9999)}"
    
    # Chat messages are short-lived
    for i in range(count):
        days_ago = random.randint(0, 60)
        created_at = now - timedelta(days=days_ago)
        
        if days_ago < 7:
            importance = random.uniform(0.5, 0.8)
            access_count = random.randint(1, 10)
        elif days_ago < 30:
            importance = random.uniform(0.3, 0.6)
            access_count = random.randint(0, 5)
        else:
            importance = random.uniform(0.1, 0.4)
            access_count = random.randint(0, 2)
        
        rehearsal_count = min(access_count // 4, random.randint(0, 3))
        
        days_since_access = min(days_ago, random.randint(0, max(1, days_ago)))
        last_accessed_at = now - timedelta(days=days_since_access) if access_count > 0 else None
        
        role = "user" if i % 2 == 0 else "assistant"
        content = random.choice(CHAT_MESSAGES)
        
        message = ChatMessage(
            organization_id=org_id,
            user_id=user_id,
            session_id=session_id,
            role=role,
            content=content,
            importance_score=importance,
            access_count=access_count,
            last_accessed_at=last_accessed_at,
            rehearsal_count=rehearsal_count,
            metadata_={
                "timestamp": created_at.isoformat(),
                "synthetic": True
            }
        )
        
        messages.append(message)
        session.add(message)
    
    session.commit()
    print_success(f"Created {len(messages)} chat messages")
    return len(messages)


def print_statistics(session, org_id, user_id):
    """Print statistics about generated data"""
    print_header("Generated Data Statistics")
    
    from mirix.services.temporal_reasoning_service import temporal_service
    from mirix.services.memory_decay_task import MEMORY_TYPES
    
    now = datetime.now(timezone.utc)
    total_memories = 0
    forgettable_count = 0
    
    for memory_type in MEMORY_TYPES:
        query = session.query(memory_type).filter(
            memory_type.organization_id == org_id
        )
        
        if user_id:
            query = query.filter(memory_type.user_id == user_id)
        
        memories = query.all()
        count = len(memories)
        total_memories += count
        
        if count > 0:
            # Calculate statistics
            avg_age = sum(temporal_service.calculate_age_in_days(m, now) for m in memories) / count
            avg_importance = sum(m.importance_score for m in memories) / count
            avg_access = sum(m.access_count for m in memories) / count
            
            # Count forgettable
            forgettable = sum(1 for m in memories if temporal_service.should_delete(m, now)[0])
            forgettable_count += forgettable
            
            print_info(f"{memory_type.__name__}:")
            print(f"    Total: {count}")
            print(f"    Avg Age: {avg_age:.1f} days")
            print(f"    Avg Importance: {avg_importance:.3f}")
            print(f"    Avg Access Count: {avg_access:.1f}")
            print(f"    Forgettable: {forgettable} ({forgettable/count*100:.1f}%)")
    
    print_success(f"\nTotal memories created: {total_memories}")
    print_success(f"Forgettable memories: {forgettable_count} ({forgettable_count/total_memories*100:.1f}%)")
    print_info(f"\nOrganization ID: {org_id}")
    print_info(f"User ID: {user_id}")


def main():
    """Main execution"""
    parser = argparse.ArgumentParser(description="Generate synthetic test data for MIRIX temporal memory")
    parser.add_argument("--org-id", required=True, help="Organization ID")
    parser.add_argument("--user-id", required=True, help="User ID")
    parser.add_argument("--episodic", type=int, default=30, help="Number of episodic memories (default: 30)")
    parser.add_argument("--semantic", type=int, default=20, help="Number of semantic memories (default: 20)")
    parser.add_argument("--procedural", type=int, default=15, help="Number of procedural memories (default: 15)")
    parser.add_argument("--resource", type=int, default=10, help="Number of resource memories (default: 10)")
    parser.add_argument("--knowledge", type=int, default=10, help="Number of knowledge vault items (default: 10)")
    parser.add_argument("--chat", type=int, default=25, help="Number of chat messages (default: 25)")
    
    args = parser.parse_args()
    
    print_header("MIRIX Synthetic Test Data Generator")
    print_info(f"Organization ID: {args.org_id}")
    print_info(f"User ID: {args.user_id}")
    print_info(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        with db_context() as session:
            # Ensure org and user exist
            print_header("Ensuring Organization and User Exist")
            org, user = ensure_org_and_user_exist(session, args.org_id, args.user_id)
            
            # Generate different types of memories
            total = 0
            total += create_episodic_memories(session, args.org_id, args.user_id, args.episodic)
            total += create_semantic_memories(session, args.org_id, args.user_id, args.semantic)
            total += create_procedural_memories(session, args.org_id, args.user_id, args.procedural)
            total += create_resource_memories(session, args.org_id, args.user_id, args.resource)
            total += create_knowledge_vault_items(session, args.org_id, args.user_id, args.knowledge)
            total += create_chat_messages(session, args.org_id, args.user_id, args.chat)
            
            # Print statistics
            print_statistics(session, args.org_id, args.user_id)
            
            print_header("SUCCESS!")
            print_success("Synthetic test data generated successfully!")
            print_info(f"Total memories created: {total}")
            print_info("\nNext steps:")
            print_info("1. Launch Streamlit dashboard: streamlit run streamlit_app.py")
            print_info(f"2. Enter Organization ID: {args.org_id}")
            print_info(f"3. Enter User ID: {args.user_id}")
            print_info("4. Explore the Dashboard, Analytics, and Cleanup tabs")
            
    except Exception as e:
        print_error(f"Error generating data: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

