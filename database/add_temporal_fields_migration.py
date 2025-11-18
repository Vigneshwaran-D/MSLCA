#!/usr/bin/env python3
"""
Temporal Fields Migration Script for Mirix

Adds temporal reasoning fields (access_count, last_accessed_at, importance_score, rehearsal_count)
to all memory tables (episodic_memory, semantic_memory, procedural_memory, resource_memory, knowledge_vault).
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


def check_column_exists(cursor, table_name, column_name, is_postgres=False):
    """Check if a column exists in a table"""
    if is_postgres:
        cursor.execute(
            """
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = %s AND column_name = %s
            """,
            (table_name, column_name),
        )
        return cursor.fetchone() is not None
    else:
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [row[1] for row in cursor.fetchall()]
        return column_name in columns


def add_temporal_fields_sqlite(conn):
    """Add temporal fields to all memory tables in SQLite"""
    cursor = conn.cursor()

    tables = [
        "episodic_memory",
        "semantic_memory",
        "procedural_memory",
        "resource_memory",
        "knowledge_vault",
    ]

    temporal_fields = [
        ("access_count", "INTEGER NOT NULL DEFAULT 0"),
        ("last_accessed_at", "DATETIME"),
        ("importance_score", "REAL NOT NULL DEFAULT 0.5"),
        ("rehearsal_count", "INTEGER NOT NULL DEFAULT 0"),
    ]

    for table in tables:
        print(f"Processing table: {table}")

        # Check if table exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table,)
        )
        if not cursor.fetchone():
            print(f"  Table {table} does not exist, skipping")
            continue

        for field_name, field_type in temporal_fields:
            if check_column_exists(cursor, table, field_name, is_postgres=False):
                print(f"  Column {field_name} already exists in {table}, skipping")
                continue

            print(f"  Adding column {field_name} to {table}")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type}")

        print(f"  ✓ Table {table} updated")

    conn.commit()
    print("SQLite migration completed successfully")


def add_temporal_fields_postgresql(conn):
    """Add temporal fields to all memory tables in PostgreSQL"""
    cursor = conn.cursor()

    tables = [
        "episodic_memory",
        "semantic_memory",
        "procedural_memory",
        "resource_memory",
        "knowledge_vault",
    ]

    temporal_fields = [
        ("access_count", "INTEGER NOT NULL DEFAULT 0"),
        ("last_accessed_at", "TIMESTAMP WITH TIME ZONE"),
        ("importance_score", "DOUBLE PRECISION NOT NULL DEFAULT 0.5"),
        ("rehearsal_count", "INTEGER NOT NULL DEFAULT 0"),
    ]

    for table in tables:
        print(f"Processing table: {table}")

        # Check if table exists
        cursor.execute(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public' AND tablename = %s",
            (table,),
        )
        if not cursor.fetchone():
            print(f"  Table {table} does not exist, skipping")
            continue

        for field_name, field_type in temporal_fields:
            if check_column_exists(cursor, table, field_name, is_postgres=True):
                print(f"  Column {field_name} already exists in {table}, skipping")
                continue

            print(f"  Adding column {field_name} to {table}")
            cursor.execute(
                f"ALTER TABLE {table} ADD COLUMN {field_name} {field_type}"
            )

        print(f"  ✓ Table {table} updated")

    # Create indexes for better query performance
    print("Creating indexes on temporal fields...")

    index_definitions = [
        ("idx_episodic_last_accessed", "episodic_memory", "last_accessed_at"),
        ("idx_episodic_importance", "episodic_memory", "importance_score"),
        ("idx_semantic_last_accessed", "semantic_memory", "last_accessed_at"),
        ("idx_semantic_importance", "semantic_memory", "importance_score"),
        ("idx_procedural_last_accessed", "procedural_memory", "last_accessed_at"),
        ("idx_procedural_importance", "procedural_memory", "importance_score"),
        ("idx_resource_last_accessed", "resource_memory", "last_accessed_at"),
        ("idx_resource_importance", "resource_memory", "importance_score"),
        ("idx_knowledge_last_accessed", "knowledge_vault", "last_accessed_at"),
        ("idx_knowledge_importance", "knowledge_vault", "importance_score"),
    ]

    for index_name, table_name, column_name in index_definitions:
        try:
            cursor.execute(
                f"CREATE INDEX IF NOT EXISTS {index_name} ON {table_name} ({column_name})"
            )
            print(f"  ✓ Created index {index_name}")
        except Exception as e:
            print(f"  Warning: Could not create index {index_name}: {e}")

    conn.commit()
    print("PostgreSQL migration completed successfully")


def run_migration():
    """Run the migration based on database type"""
    print("=" * 60)
    print("Mirix Temporal Fields Migration")
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
            add_temporal_fields_postgresql(conn)

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
            add_temporal_fields_sqlite(conn)

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
        print("2. Temporal reasoning is now enabled")
        print("3. Configure settings in mirix/settings.py if needed")
    else:
        print("Migration failed. Please check the error messages above.")
    print("=" * 60)


if __name__ == "__main__":
    main()

