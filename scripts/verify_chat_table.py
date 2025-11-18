"""Verify chat_messages table exists in database"""
import sqlite3
import sys
import os

# Database path
db_path = os.path.expanduser("~/.mirix/sqlite.db")

try:
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if chat_messages table exists
    cursor.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='chat_messages'
    """)
    
    result = cursor.fetchone()
    
    if result:
        print("[SUCCESS] chat_messages table exists!")
        
        # Get table schema
        cursor.execute("PRAGMA table_info(chat_messages)")
        columns = cursor.fetchall()
        
        print(f"\nTable has {len(columns)} columns:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Check for temporal fields
        temporal_fields = ['access_count', 'last_accessed_at', 'importance_score', 'rehearsal_count']
        has_temporal = all(any(col[1] == field for col in columns) for field in temporal_fields)
        
        if has_temporal:
            print("\n[SUCCESS] All temporal reasoning fields present!")
        else:
            print("\n[WARNING] Some temporal fields may be missing")
            
        sys.exit(0)
    else:
        print("[ERROR] chat_messages table does NOT exist!")
        print("\nAvailable tables:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        sys.exit(1)
        
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
finally:
    if 'conn' in locals():
        conn.close()

