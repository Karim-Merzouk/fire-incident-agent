import sqlite3
import os

def check_table_structure():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check structure of disease tables
        disease_tables = [
            'disease_disease', 'disease_symptom', 'disease_testing_device',
            'disease_case', 'disease_demographic', 'disease_testing_report'
        ]
        
        for table in disease_tables:
            print(f"\n📋 {table.upper()}:")
            print("-" * 40)
            cursor.execute(f"PRAGMA table_info({table})")
            columns = cursor.fetchall()
            for col in columns:
                print(f"  {col[1]} ({col[2]})")
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_table_structure()
