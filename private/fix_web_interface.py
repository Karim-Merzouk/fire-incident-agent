import sqlite3
import os
import uuid
from datetime import datetime

def fix_web_interface_data():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 FIXING WEB INTERFACE DATA VISIBILITY...")
        print("=" * 50)
        
        # Check current data state
        cursor.execute("SELECT COUNT(*) FROM disease_disease")
        diseases_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM disease_case")
        cases_count = cursor.fetchone()[0]
        
        print(f"Current diseases in DB: {diseases_count}")
        print(f"Current cases in DB: {cases_count}")
        
        # Ensure disease has proper UUID and other required fields
        print("\n1. Updating disease record...")
        cursor.execute("""
            UPDATE disease_disease 
            SET uuid = ?, 
                deleted = 'F',
                approved_by = 1,
                owned_by_user = 1,
                realm_entity = 1
            WHERE id = 1
        """, (str(uuid.uuid4()),))
        
        # Update all symptoms with proper UUIDs
        print("2. Updating symptoms...")
        cursor.execute("SELECT id FROM disease_symptom WHERE disease_id = 1")
        symptom_ids = [row[0] for row in cursor.fetchall()]
        
        for symptom_id in symptom_ids:
            cursor.execute("""
                UPDATE disease_symptom 
                SET uuid = ?, 
                    deleted = 'F',
                    approved_by = 1,
                    owned_by_user = 1,
                    realm_entity = 1
                WHERE id = ?
            """, (str(uuid.uuid4()), symptom_id))
        
        # Update all testing devices
        print("3. Updating testing devices...")
        cursor.execute("SELECT id FROM disease_testing_device WHERE disease_id = 1")
        device_ids = [row[0] for row in cursor.fetchall()]
        
        for device_id in device_ids:
            cursor.execute("""
                UPDATE disease_testing_device 
                SET uuid = ?, 
                    deleted = 'F',
                    approved_by = 1,
                    owned_by_user = 1,
                    realm_entity = 1
                WHERE id = ?
            """, (str(uuid.uuid4()), device_id))
        
        # Update all demographics
        print("4. Updating demographics...")
        cursor.execute("SELECT id FROM disease_demographic")
        demo_ids = [row[0] for row in cursor.fetchall()]
        
        for demo_id in demo_ids:
            cursor.execute("""
                UPDATE disease_demographic 
                SET uuid = ?, 
                    deleted = 'F',
                    approved_by = 1,
                    owned_by_user = 1,
                    realm_entity = 1
                WHERE id = ?
            """, (str(uuid.uuid4()), demo_id))
        
        # Update all cases - most important for web interface
        print("5. Updating cases with proper visibility settings...")
        cursor.execute("SELECT id FROM disease_case WHERE disease_id = 1")
        case_ids = [row[0] for row in cursor.fetchall()]
        
        for case_id in case_ids:
            cursor.execute("""
                UPDATE disease_case 
                SET deleted = 'F',
                    approved_by = 1,
                    owned_by_user = 1,
                    realm_entity = 1
                WHERE id = ?
            """, (case_id,))
        
        # Update testing reports
        print("6. Updating testing reports...")
        cursor.execute("SELECT id FROM disease_testing_report WHERE disease_id = 1")
        report_ids = [row[0] for row in cursor.fetchall()]
        
        for report_id in report_ids:
            cursor.execute("""
                UPDATE disease_testing_report 
                SET deleted = 'F',
                    approved_by = 1,
                    owned_by_user = 1,
                    realm_entity = 1
                WHERE id = ?
            """, (report_id,))
        
        # Add some persons for the cases (required for proper display)
        print("7. Creating person records for cases...")
        
        # First, let's see if there are any existing persons
        cursor.execute("SELECT id FROM pr_person LIMIT 5")
        existing_persons = cursor.fetchall()
        
        if existing_persons:
            print(f"   Found {len(existing_persons)} existing persons, linking to cases...")
            # Link existing persons to cases
            cursor.execute("SELECT id FROM disease_case WHERE disease_id = 1 AND person_id IS NULL")
            unlinked_cases = cursor.fetchall()
            
            for i, (case_id,) in enumerate(unlinked_cases):
                person_id = existing_persons[i % len(existing_persons)][0]
                cursor.execute("UPDATE disease_case SET person_id = ? WHERE id = ?", (person_id, case_id))
        else:
            print("   Creating new person records...")
            # Create some basic person records
            for i in range(5):
                cursor.execute("""
                    INSERT INTO pr_person 
                    (uuid, deleted, created_by, created_on, modified_by, modified_on)
                    VALUES (?, 'F', 1, ?, 1, ?)
                """, (str(uuid.uuid4()), datetime.now().isoformat(), datetime.now().isoformat()))
                
                person_id = cursor.lastrowid
                
                # Link to some cases
                cursor.execute("""
                    UPDATE disease_case 
                    SET person_id = ? 
                    WHERE disease_id = 1 AND person_id IS NULL 
                    LIMIT 5
                """, (person_id,))
        
        conn.commit()
        conn.close()
        
        print("\n✅ WEB INTERFACE DATA FIXES COMPLETED!")
        print("=" * 50)
        print("🌐 Try refreshing the web interface:")
        print("   • Cases: http://127.0.0.1:8000/eden/disease/case")
        print("   • Diseases: http://127.0.0.1:8000/eden/disease")
        
    except Exception as e:
        print(f"❌ Error fixing data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    fix_web_interface_data()
