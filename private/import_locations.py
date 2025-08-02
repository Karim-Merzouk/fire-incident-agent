#!/usr/bin/env python3
"""
Import COVID-19 locations into Sahana Eden database
"""

import csv
import sqlite3
import os
from datetime import datetime

def import_locations_to_database():
    """Import location data from CSV to SQLite database"""
    
    # Database path
    db_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db"
    csv_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/private/templates/Disease/COVID-19/gis_locations_covid.csv"
    
    if not os.path.exists(db_path):
        print("Database not found. Please start Sahana Eden first.")
        return
    
    if not os.path.exists(csv_path):
        print("Location CSV file not found.")
        return
    
    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Importing COVID-19 locations...")
    
    try:
        # Read CSV file
        with open(csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for i, row in enumerate(reader, 1):
                # Insert location data
                name = row['Name']
                lat = float(row['Lat']) if row['Lat'] else None
                lon = float(row['Lon']) if row['Lon'] else None
                comments = row['Comments']
                
                cursor.execute("""
                    INSERT OR REPLACE INTO gis_location 
                    (id, name, lat, lon, comments, created_on)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (i, name, lat, lon, comments, datetime.now()))
                
                print(f"Imported: {name}")
        
        conn.commit()
        print(f"✅ Successfully imported {i} locations!")
        
        # Show what was imported
        cursor.execute("SELECT COUNT(*) FROM gis_location WHERE comments LIKE '%COVID%'")
        count = cursor.fetchone()[0]
        print(f"Total COVID-19 related locations in database: {count}")
        
    except Exception as e:
        print(f"❌ Error importing locations: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    import_locations_to_database()
