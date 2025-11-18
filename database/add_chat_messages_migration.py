#!/usr/bin/env python3
"""
Chat Messages Table Migration Script for Mirix

Creates the chat_messages table with temporal reasoning fields for storing
conversational AI interactions.
"""

import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

# Add parent directory to path to import mirix modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from mirix.settings import settings


def backup_database_file(db_path):
    """Create a backup of the SQLite database file"""
    backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(db_path, backup_path)
    print(f"Created backup: {backup_path}")
    return backup_path


def check_table_exists(cursor, table_name, is_postgres=False):
    """Check if a table exists"""
    if is_postgres:
        cursor.execute(
            """
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public' AND tablename = %s
            """,
            (table_name,),
        )
        return cursor.fetchone() is not None
    else:
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,)
        )
        return cursor.fetchone() is not None


def create_chat_messages_table_sqlite(conn):
    """Create chat_messages table in SQLite"""
    cursor = conn.cursor()

    if check_table_exists(cursor, "chat_messages", is_postgres=False):
        print("  Table 'chat_messages' already exists, skipping creation")
        return

    print("Creating chat_messages table...")

    cursor.execute("""
        CREATE TABLE chat_messages (
            id TEXT PRIMARY KEY,
            session_id TEXT NOT NULL,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at DATETIME NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0,
            last_accessed_at DATETIME,
            importance_score REAL NOT NULL DEFAULT 0.5,
            rehearsal_count INTEGER NOT NULL DEFAULT 0,
            metadata_ TEXT,
            agent_id TEXT,
            parent_message_id TEXT,
            embedding_config TEXT,
            content_embedding BLOB,
            last_modify TEXT NOT NULL,
            organization_id TEXT NOT NULL,
            user_id TEXT NOT NULL,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX idx_chat_session_id ON chat_messages(session_id)")
    cursor.execute("CREATE INDEX idx_chat_created_at ON chat_messages(created_at)")
    cursor.execute("CREATE INDEX idx_chat_importance ON chat_messages(importance_score)")
    cursor.execute("CREATE INDEX idx_chat_last_accessed ON chat_messages(last_accessed_at)")
    cursor.execute("CREATE INDEX idx_chat_user_id ON chat_messages(user_id)")

    conn.commit()
    print("  ✓ Table 'chat_messages' created successfully")


def create_chat_messages_table_postgresql(conn):
    """Create chat_messages table in PostgreSQL"""
    cursor = conn.cursor()

    if check_table_exists(cursor, "chat_messages", is_postgres=True):
        print("  Table 'chat_messages' already exists, skipping creation")
        return

    print("Creating chat_messages table...")

    cursor.execute("""
        CREATE TABLE chat_messages (
            id VARCHAR PRIMARY KEY,
            session_id VARCHAR NOT NULL,
            role VARCHAR NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP WITH TIME ZONE NOT NULL,
            access_count INTEGER NOT NULL DEFAULT 0,
            last_accessed_at TIMESTAMP WITH TIME ZONE,
            importance_score DOUBLE PRECISION NOT NULL DEFAULT 0.5,
            rehearsal_count INTEGER NOT NULL DEFAULT 0,
            metadata_ JSONB,
            agent_id VARCHAR,
            parent_message_id VARCHAR,
            embedding_config JSONB,
            content_embedding vector(1536),
            last_modify JSONB NOT NULL,
            organization_id VARCHAR NOT NULL,
            user_id VARCHAR NOT NULL,
            FOREIGN KEY (organization_id) REFERENCES organizations(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Create indexes
    cursor.execute("CREATE INDEX idx_chat_session_id ON chat_messages(session_id)")
    cursor.execute("CREATE INDEX idx_chat_created_at ON chat_messages(created_at)")
    cursor.execute("CREATE INDEX idx_chat_importance ON chat_messages(importance_score)")
    cursor.execute("CREATE INDEX idx_chat_last_accessed ON chat_messages(last_accessed_at)")
    cursor.execute("CREATE INDEX idx_chat_user_id ON chat_messages(user_id)")

    # Create vector similarity index if using pgvector
    try:
        cursor.execute(
            "CREATE INDEX idx_chat_content_embedding ON chat_messages USING ivfflat (content_embedding vector_cosine_ops)"
        )
        print("  ✓ Created vector similarity index")
    except Exception as e:
        print(f"  Warning: Could not create vector index: {e}")

    conn.commit()
    print("  ✓ Table 'chat_messages' created successfully")


def run_migration():
    """Run the migration based on database type"""
    print("=" * 60)
    print("Mirix Chat Messages Table Migration")
    print("=" * 60)
    print()

    # Check if using PostgreSQL or SQLite
    pg_uri = settings.mirix_pg_uri_no_default

    if pg_uri:
        print("Detected PostgreSQL database")
        print(f"Connection URI: {pg_uri.split('@')[1] if '@' in pg_uri else 'hidden'}")
        print()

        # Import PostgreSQL adapter
        try:
            import psycopg2
        except ImportError:
            print("Error: psycopg2 not installed")
            print("Install with: pip install psycopg2-binary")
            return False

        try:
            # Convert pg8000 URI to psycopg2 format if needed
            conn_uri = pg_uri.replace("postgresql+pg8000://", "postgresql://")

            print("Connecting to PostgreSQL...")
            conn = psycopg2.connect(conn_uri)
            conn.autocommit = False

            print("Running migration...")
            create_chat_messages_table_postgresql(conn)

            conn.close()
            print()
            print("✓ PostgreSQL migration completed successfully!")
            return True

        except Exception as e:
            print(f"Error during PostgreSQL migration: {e}")
            import traceback

            traceback.print_exc()
            return False

    else:
        print("Detected SQLite database")
        db_path = settings.mirix_dir / "mirix.db"
        print(f"Database path: {db_path}")
        print()

        if not os.path.exists(db_path):
            print(f"Error: Database file not found at {db_path}")
            return False

        import sqlite3

        try:
            # Create backup
            backup_path = backup_database_file(db_path)
            print()

            print("Connecting to SQLite...")
            conn = sqlite3.connect(db_path)

            print("Running migration...")
            create_chat_messages_table_sqlite(conn)

            conn.close()
            print()
            print("✓ SQLite migration completed successfully!")
            print(f"  Backup available at: {backup_path}")
            return True

        except Exception as e:
            print(f"Error during SQLite migration: {e}")
            import traceback

            traceback.print_exc()

            # Attempt to restore from backup
            if "backup_path" in locals():
                print()
                print("Attempting to restore from backup...")
                try:
                    shutil.copy2(backup_path, db_path)
                    print("✓ Database restored from backup")
                except Exception as restore_error:
                    print(f"Error restoring from backup: {restore_error}")

            return False


def main():
    """Main entry point"""
    import sys
    
    # Check for --yes flag
    auto_yes = "--yes" in sys.argv or "-y" in sys.argv
    
    if not auto_yes:
        print()
        response = input("This will modify the database. Continue? (yes/no): ")
        if response.lower() not in ["yes", "y"]:
            print("Migration cancelled")
            return

    print()
    success = run_migration()

    print()
    print("=" * 60)
    if success:
        print("Migration completed successfully!")
        print()
        print("Next steps:")
        print("1. Restart your Mirix application")
        print("2. Chat feature is now available in Streamlit UI")
        print("3. All chat messages will be stored with temporal reasoning")
    else:
        print("Migration failed. Please check the error messages above.")
    print("=" * 60)


if __name__ == "__main__":
    main()

