
import sqlite3
import os

# Path to database
db_path = os.path.join('instance', 'app.db')

def check_and_add_column(cursor, table, column, col_type):
    """Check if a column exists, if not add it."""
    print(f"Checking {table}.{column}...")
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    
    if column not in columns:
        print(f"  Adding column {column}...")
        try:
            # SQLite doesn't support adding JSON type directly in older versions, usually TEXT or just default
            # But Flask-SQLAlchemy usually maps it. JSON in SQLite is just TEXT.
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {col_type}")
            print("  Done.")
            return True
        except Exception as e:
            print(f"  Error adding column: {e}")
            return False
    else:
        print("  Column already exists.")
        return False

def migrate():
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. No migration needed (run reset_db.py instead).")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"Connected to database: {db_path}")
    
    changes = False
    
    # 1. Add interview_questions
    # We use TEXT because SQLite stores JSON as TEXT
    if check_and_add_column(cursor, 'analyses', 'interview_questions', 'TEXT'):
        changes = True
        
    # 2. Add skill_resources
    if check_and_add_column(cursor, 'analyses', 'skill_resources', 'TEXT'):
        changes = True

    if changes:
        conn.commit()
        print("\nMigration completed successfully.")
    else:
        print("\nNo changes needed.")
        
    conn.close()

if __name__ == "__main__":
    migrate()
