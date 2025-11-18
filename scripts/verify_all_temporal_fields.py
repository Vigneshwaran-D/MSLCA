"""Verify all memory tables have temporal fields"""
import sqlite3
import os

db_path = os.path.expanduser("~/.mirix/sqlite.db")

# Memory tables that should have temporal fields
MEMORY_TABLES = [
    'episodic_memory',
    'semantic_memory',
    'procedural_memory',
    'resource_memory',
    'knowledge_vault',
    'chat_messages'
]

TEMPORAL_FIELDS = ['access_count', 'last_accessed_at', 'importance_score', 'rehearsal_count']

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("="*60)
    print("TEMPORAL FIELDS VERIFICATION")
    print("="*60)
    
    all_good = True
    
    for table in MEMORY_TABLES:
        # Check if table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
        if not cursor.fetchone():
            print(f"\n[ERROR] Table '{table}' does not exist!")
            all_good = False
            continue
        
        # Get columns
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        # Check temporal fields
        missing = [field for field in TEMPORAL_FIELDS if field not in column_names]
        
        if missing:
            print(f"\n[ERROR] {table}: Missing fields: {', '.join(missing)}")
            all_good = False
        else:
            print(f"\n[SUCCESS] {table}: All temporal fields present ({len(columns)} total columns)")
    
    print("\n" + "="*60)
    if all_good:
        print("[SUCCESS] All memory tables have temporal reasoning fields!")
        print("="*60)
    else:
        print("[ERROR] Some tables are missing temporal fields!")
        print("="*60)
    
    conn.close()
    
except Exception as e:
    print(f"[ERROR] {e}")
    import traceback
    traceback.print_exc()

