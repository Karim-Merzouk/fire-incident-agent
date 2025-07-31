import sqlite3
import os

def check_disease_tables():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables with 'disease' in the name
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%disease%'")
        disease_tables = cursor.fetchall()
        
        print("DISEASE TABLES FOUND:")
        print("=" * 40)
        
        if disease_tables:
            for table in disease_tables:
                table_name = table[0]
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"  {table_name}: {count} records")
        else:
            print("  No disease tables found yet.")
            print("  Server may need more time to initialize.")
        
        # Also check for any new tables since last check
        cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
        total_tables = cursor.fetchone()[0]
        print(f"\nTotal tables in database: {total_tables}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_disease_tables()
