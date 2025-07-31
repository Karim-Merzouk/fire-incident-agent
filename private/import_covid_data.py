import sqlite3
import os
import csv
from datetime import datetime, timedelta
import random
import uuid

def import_covid_data():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🦠 IMPORTING COVID-19 DATA...")
        print("=" * 50)
        
        # 1. Import COVID-19 Disease
        print("📝 Importing COVID-19 disease definition...")
        cursor.execute("""
            INSERT OR REPLACE INTO disease_disease 
            (name, description, created_by, created_on, modified_by, modified_on)
            VALUES (?, ?, 1, ?, 1, ?)
        """, (
            "COVID-19", 
            "Coronavirus Disease 2019 (COVID-19) is an infectious disease caused by SARS-CoV-2 virus.",
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        disease_id = cursor.lastrowid
        print(f"   ✅ COVID-19 disease created (ID: {disease_id})")
        
        # 2. Import Symptoms
        symptoms = [
            "Fever", "Dry cough", "Fatigue", "Loss of taste", "Loss of smell",
            "Sore throat", "Headache", "Aches and pains", "Diarrhea", "Rash",
            "Discoloration of fingers", "Red or irritated eyes", "Difficulty breathing",
            "Shortness of breath", "Loss of speech", "Loss of mobility", "Confusion",
            "Chest pain", "Nausea", "Vomiting"
        ]
        
        print("🤒 Importing COVID-19 symptoms...")
        for symptom in symptoms:
            cursor.execute("""
                INSERT OR REPLACE INTO disease_symptom 
                (name, disease_id, created_by, created_on, modified_by, modified_on)
                VALUES (?, ?, 1, ?, 1, ?)
            """, (symptom, disease_id, datetime.now().isoformat(), datetime.now().isoformat()))
        print(f"   ✅ {len(symptoms)} symptoms imported")
        
        # 3. Import Testing Devices
        testing_devices = [
            ("RT-PCR Test", "PCR01", "Molecular", "T", "T", "Laboratory"),
            ("Rapid Antigen Test", "RAT01", "Antigen", "T", "T", "Point of Care"),
            ("Antibody Test", "AB01", "Serological", "T", "T", "Laboratory"),
            ("Saliva Test", "SAL01", "Molecular", "T", "T", "Point of Care"),
            ("Home Test Kit", "HTK01", "Antigen", "T", "T", "Home Use"),
            ("Molecular Test", "MOL01", "Molecular", "T", "T", "Laboratory")
        ]
        
        print("🔬 Importing testing devices...")
        for device_name, code, device_class, approved, available, source in testing_devices:
            cursor.execute("""
                INSERT OR REPLACE INTO disease_testing_device 
                (name, code, device_class, approved, available, source, disease_id, created_by, created_on, modified_by, modified_on)
                VALUES (?, ?, ?, ?, ?, ?, ?, 1, ?, 1, ?)
            """, (device_name, code, device_class, approved, available, source, disease_id, datetime.now().isoformat(), datetime.now().isoformat()))
        print(f"   ✅ {len(testing_devices)} testing devices imported")
        
        # 4. Import Demographics
        demographics = [
            ("AG09", "Age 0-9"), ("AG19", "Age 10-19"), ("AG29", "Age 20-29"), 
            ("AG39", "Age 30-39"), ("AG49", "Age 40-49"), ("AG59", "Age 50-59"), 
            ("AG69", "Age 60-69"), ("AG79", "Age 70-79"), ("AG80", "Age 80+"), 
            ("MALE", "Male"), ("FEM", "Female"), ("HCW", "Healthcare Worker"), 
            ("ESW", "Essential Worker"), ("IMC", "Immunocompromised")
        ]
        
        print("👥 Importing demographics...")
        for code, demo_name in demographics:
            cursor.execute("""
                INSERT OR REPLACE INTO disease_demographic 
                (code, name, created_by, created_on, modified_by, modified_on)
                VALUES (?, ?, 1, ?, 1, ?)
            """, (code, demo_name, datetime.now().isoformat(), datetime.now().isoformat()))
        print(f"   ✅ {len(demographics)} demographic categories imported")
        
        # 5. Import Sample Cases
        print("🏥 Importing sample COVID-19 cases...")
        illness_statuses = ["Symptomatic", "Asymptomatic", "Recovered", "Deceased"]
        diagnosis_statuses = ["Confirmed", "Probable", "Suspected", "Under Investigation"]
        monitoring_levels = ["Self-monitoring", "Active monitoring", "Direct observation", "Hospitalized"]
        
        for i in range(25):  # Create 25 sample cases
            # Random date in the last 2 years
            start_date = datetime.now() - timedelta(days=730)
            random_days = random.randint(0, 730)
            case_date = start_date + timedelta(days=random_days)
            
            illness_status = random.choice(illness_statuses)
            diagnosis_status = random.choice(diagnosis_statuses)
            monitoring_level = random.choice(monitoring_levels)
            hospitalized = random.choice(['T', 'F'])
            intensive_care = random.choice(['T', 'F']) if hospitalized == 'T' else 'F'
            
            case_number = f"COVID-{datetime.now().year}-{i+1:04d}"
            
            cursor.execute("""
                INSERT INTO disease_case 
                (case_number, disease_id, illness_status, diagnosis_status, diagnosis_date, 
                 monitoring_level, hospitalized, intensive_care, uuid, created_by, created_on, modified_by, modified_on)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?, 1, ?)
            """, (
                case_number, disease_id, illness_status, diagnosis_status, case_date.date().isoformat(),
                monitoring_level, hospitalized, intensive_care, str(uuid.uuid4()),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
        print(f"   ✅ 25 sample cases imported")
        
        # 6. Import Sample Testing Reports
        print("📊 Importing sample testing reports...")
        
        for i in range(50):  # Create 50 test reports
            test_date = datetime.now() - timedelta(days=random.randint(0, 365))
            tests_total = random.randint(10, 500)
            tests_positive = random.randint(0, tests_total // 3)  # Roughly 0-33% positive rate
            
            cursor.execute("""
                INSERT INTO disease_testing_report 
                (disease_id, date, tests_total, tests_positive, uuid, created_by, created_on, modified_by, modified_on)
                VALUES (?, ?, ?, ?, ?, 1, ?, 1, ?)
            """, (
                disease_id, test_date.date().isoformat(), tests_total, tests_positive, str(uuid.uuid4()),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
        print(f"   ✅ 50 testing reports imported")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 COVID-19 DATA IMPORT COMPLETED!")
        print("=" * 50)
        
        # Show final counts
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        tables_to_check = [
            'disease_disease', 'disease_symptom', 'disease_testing_device',
            'disease_demographic', 'disease_case', 'disease_testing_report'
        ]
        
        print("📊 FINAL DATABASE COUNTS:")
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   {table}: {count} records")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error importing data: {e}")
        return False
    
    return True

if __name__ == "__main__":
    import_covid_data()
