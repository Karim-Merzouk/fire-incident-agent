#!/usr/bin/env python3
"""
Database Explorer - Check what tables exist in the Sahana Eden database
"""

import sqlite3
import os

def explore_database():
    """Explore the Sahana Eden database structure"""
    
    db_path = "../databases/storage.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database file not found: {db_path}")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print("📊 SAHANA EDEN DATABASE STRUCTURE")
        print("=" * 50)
        print(f"Database path: {db_path}")
        print(f"Total tables: {len(tables)}")
        print()
        
        # Show first 20 tables
        print("📋 AVAILABLE TABLES:")
        for i, (table_name,) in enumerate(tables[:20]):
            print(f"{i+1:2d}. {table_name}")
        
        if len(tables) > 20:
            print(f"    ... and {len(tables)-20} more tables")
        
        print()
        
        # Look for tables related to our use case
        relevant_keywords = ['person', 'location', 'shelter', 'incident', 'fire', 'disease', 
                           'case', 'event', 'resource', 'volunteer', 'org', 'asset', 'req']
        
        print("🔍 RELEVANT TABLES FOR EMERGENCY RESPONSE:")
        relevant_tables = []
        for table_name, in tables:
            for keyword in relevant_keywords:
                if keyword in table_name.lower():
                    relevant_tables.append(table_name)
                    break
        
        for table in sorted(set(relevant_tables))[:15]:
            print(f"• {table}")
        
        print()
        
        # Check some key tables that likely exist
        key_tables = ['pr_person', 'gis_location', 'org_organisation', 'disease_case']
        print("🔍 CHECKING KEY TABLES:")
        
        for table in key_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"✅ {table}: {count} records")
                
                # Show sample structure
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                print(f"   Columns: {', '.join([col[1] for col in columns[:5]])}{'...' if len(columns) > 5 else ''}")
                
            except sqlite3.Error as e:
                print(f"❌ {table}: Table doesn't exist")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database exploration failed: {e}")

if __name__ == "__main__":
    explore_database()
