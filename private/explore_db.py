#!/usr/bin/env python3
"""
Simple database explorer for Sahana Eden
"""

import sqlite3
import os

def explore_database():
    """Explore the current database structure"""
    
    db_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found!")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 CURRENT DATABASE CONTENTS")
    print("=" * 40)
    
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"📊 Found {len(tables)} tables in database")
        print("\n📋 TABLE LIST WITH RECORD COUNTS:")
        print("-" * 40)
        
        for table in tables:
            table_name = table[0]
            try:
                cursor.execute(f"SELECT COUNT(*) FROM `{table_name}`")
                count = cursor.fetchone()[0]
                
                # Highlight interesting tables
                if count > 0:
                    if 'disease' in table_name.lower():
                        print(f"🦠 {table_name}: {count} records")
                    elif 'location' in table_name.lower() or 'gis' in table_name.lower():
                        print(f"📍 {table_name}: {count} records")
                    elif 'auth' in table_name.lower() or 'user' in table_name.lower():
                        print(f"👤 {table_name}: {count} records")
                    elif 'stats' in table_name.lower():
                        print(f"📈 {table_name}: {count} records")
                    else:
                        print(f"📄 {table_name}: {count} records")
                else:
                    print(f"   {table_name}: {count} records")
                    
            except Exception as e:
                print(f"❌ {table_name}: Error - {e}")
        
        # Show some actual data from key tables
        print("\n" + "=" * 40)
        print("📋 SAMPLE DATA")
        print("=" * 40)
        
        # Show locations that have names
        cursor.execute("SELECT id, name, lat, lon FROM gis_location WHERE name IS NOT NULL AND name != '' LIMIT 10")
        locations = cursor.fetchall()
        if locations:
            print("\n📍 LOCATIONS:")
            for loc in locations:
                print(f"  {loc[0]}: {loc[1]} ({loc[2]}, {loc[3]})")
        
        # Show users
        cursor.execute("SELECT id, first_name, last_name, email FROM auth_user LIMIT 5")
        users = cursor.fetchall()
        if users:
            print("\n👤 USERS:")
            for user in users:
                print(f"  {user[0]}: {user[1]} {user[2]} - {user[3]}")
        
        # Check if disease tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%disease%'")
        disease_tables = cursor.fetchall()
        
        if disease_tables:
            print(f"\n🦠 DISEASE TABLES FOUND: {len(disease_tables)}")
            for table in disease_tables:
                cursor.execute(f"SELECT COUNT(*) FROM `{table[0]}`")
                count = cursor.fetchone()[0]
                print(f"  {table[0]}: {count} records")
        else:
            print("\n❌ NO DISEASE TABLES FOUND")
            print("   The Disease template may not be fully initialized.")
            print("   Please start Sahana Eden web server to create tables.")
        
    except Exception as e:
        print(f"❌ Error exploring database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    explore_database()
