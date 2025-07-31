import sqlite3
import os

def check_person_table():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("PR_PERSON TABLE STRUCTURE:")
        print("-" * 40)
        cursor.execute("PRAGMA table_info(pr_person)")
        columns = cursor.fetchall()
        for col in columns:
            required = "NOT NULL" if col[3] == 1 else "NULLABLE"
            print(f"  {col[1]} ({col[2]}) - {required}")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_person_table()
