#!/usr/bin/env python3
"""
Test database connection for Forest Fire system
"""

import os
import sqlite3

def test_database_connection():
    """Test the database connection"""
    # Get the absolute path to the databases directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, "..", "databases", "storage.db")
    db_path = os.path.abspath(db_path)
    
    print(f"Testing database at: {db_path}")
    print(f"File exists: {os.path.exists(db_path)}")
    
    if not os.path.exists(db_path):
        print("❌ Database file does not exist!")
        return False
    
    try:
        connection = sqlite3.connect(db_path)
        connection.row_factory = sqlite3.Row
        
        # Test a simple query
        cursor = connection.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 5")
        tables = cursor.fetchall()
        
        print(f"✅ Database connection successful!")
        print(f"Sample tables found: {[table[0] for table in tables]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    test_database_connection()
