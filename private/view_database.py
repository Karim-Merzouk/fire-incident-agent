#!/usr/bin/env python3
"""
View Sahana Eden Database Contents
"""

import sqlite3
import os
from datetime import datetime

def show_database_contents():
    """Display database tables and sample data"""
    
    # Database path
    db_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db"
    
    if not os.path.exists(db_path):
        print("❌ Database not found. Please start Sahana Eden first.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 SAHANA EDEN DATABASE OVERVIEW")
    print("=" * 50)
    
    try:
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = cursor.fetchall()
        
        print(f"📊 Total Tables: {len(tables)}")
        print("-" * 30)
        
        # Show disease-related tables
        disease_tables = [t[0] for t in tables if 'disease' in t[0]]
        if disease_tables:
            print("\n🦠 COVID-19/DISEASE TABLES:")
            for table in disease_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  • {table}: {count} records")
        
        # Show location tables
        location_tables = [t[0] for t in tables if 'gis' in t[0] or 'location' in t[0]]
        if location_tables:
            print("\n📍 LOCATION/GIS TABLES:")
            for table in location_tables[:10]:  # Show first 10
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  • {table}: {count} records")
        
        # Show user/auth tables
        auth_tables = [t[0] for t in tables if 'auth' in t[0] or 'pr_person' in t[0]]
        if auth_tables:
            print("\n👥 USER/PERSON TABLES:")
            for table in auth_tables[:8]:  # Show first 8
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  • {table}: {count} records")
        
        # Show statistics tables
        stats_tables = [t[0] for t in tables if 'stats' in t[0]]
        if stats_tables:
            print("\n📈 STATISTICS TABLES:")
            for table in stats_tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"  • {table}: {count} records")
        
        # Sample data from key tables
        print("\n" + "=" * 50)
        print("📋 SAMPLE DATA FROM KEY TABLES")
        print("=" * 50)
        
        # Check if gis_location has data
        cursor.execute("SELECT COUNT(*) FROM gis_location")
        location_count = cursor.fetchone()[0]
        if location_count > 0:
            print(f"\n📍 GIS_LOCATION Table ({location_count} records):")
            cursor.execute("SELECT id, name, lat, lon, comments FROM gis_location LIMIT 5")
            locations = cursor.fetchall()
            for loc in locations:
                print(f"  ID: {loc[0]}, Name: {loc[1]}, Lat: {loc[2]}, Lon: {loc[3]}")
                if loc[4]:
                    print(f"      Comments: {loc[4][:50]}...")
        
        # Check auth_user table
        cursor.execute("SELECT COUNT(*) FROM auth_user")
        user_count = cursor.fetchone()[0]
        print(f"\n👤 AUTH_USER Table ({user_count} records):")
        if user_count > 0:
            cursor.execute("SELECT id, first_name, last_name, email FROM auth_user LIMIT 3")
            users = cursor.fetchall()
            for user in users:
                print(f"  ID: {user[0]}, Name: {user[1]} {user[2]}, Email: {user[3]}")
    
        # Database file info
        file_size = os.path.getsize(db_path) / (1024 * 1024)  # Convert to MB
        print(f"\n💾 Database File Size: {file_size:.2f} MB")
        print(f"📁 Database Location: {db_path}")
        
        print("\n" + "=" * 50)
        print("🌐 WEB ACCESS URLS:")
        print("=" * 50)
        print("Main Application: http://127.0.0.1:8000/eden")
        print("Database Admin:   http://127.0.0.1:8000/admin")
        print("Disease Module:   http://127.0.0.1:8000/eden/disease")
        print("Locations:        http://127.0.0.1:8000/eden/gis/location")
        print("Users:            http://127.0.0.1:8000/eden/admin/user")
        
    except Exception as e:
        print(f"❌ Error accessing database: {e}")
    finally:
        conn.close()

def show_covid_specific_data():
    """Show COVID-19 specific data"""
    
    db_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("\n🦠 COVID-19 SPECIFIC DATA")
    print("=" * 30)
    
    try:
        # Check disease_disease table
        cursor.execute("SELECT COUNT(*) FROM disease_disease WHERE name LIKE '%COVID%' OR name LIKE '%Coronavirus%'")
        covid_diseases = cursor.fetchone()[0]
        print(f"COVID-19 Disease Records: {covid_diseases}")
        
        if covid_diseases > 0:
            cursor.execute("SELECT id, name, short_name, description FROM disease_disease WHERE name LIKE '%COVID%' OR name LIKE '%Coronavirus%'")
            diseases = cursor.fetchall()
            for disease in diseases:
                print(f"  • {disease[1]} ({disease[2]})")
                print(f"    Description: {disease[3][:60]}...")
        
        # Check disease_case table
        cursor.execute("SELECT COUNT(*) FROM disease_case")   
        case_count = cursor.fetchone()[0]
        print(f"Total Disease Cases: {case_count}")
        
        # Check disease_symptom table
        cursor.execute("SELECT COUNT(*) FROM disease_symptom")
        symptom_count = cursor.fetchone()[0]
        print(f"Disease Symptoms: {symptom_count}")
        
        if symptom_count > 0:
            cursor.execute("SELECT name, description FROM disease_symptom LIMIT 5")
            symptoms = cursor.fetchall()
            print("Sample Symptoms:")
            for symptom in symptoms:
                print(f"  • {symptom[0]}: {symptom[1] or 'No description'}")
        
    except Exception as e:
        print(f"Error getting COVID data: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    show_database_contents()
    show_covid_specific_data()
