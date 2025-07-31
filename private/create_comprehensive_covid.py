import sqlite3
import os
import uuid
from datetime import datetime, timedelta
import random

def create_comprehensive_covid_data():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🦠 CREATING COMPREHENSIVE COVID-19 DATA FOR WEB INTERFACE...")
        print("=" * 60)
        
        # First, ensure we have the main COVID-19 disease with all required fields
        print("1. Setting up COVID-19 disease definition...")
        cursor.execute("""
            INSERT OR REPLACE INTO disease_disease 
            (id, name, short_name, acronym, code, description, trace_period, watch_period,
             uuid, deleted, created_by, created_on, modified_by, modified_on, 
             approved_by, owned_by_user, realm_entity)
            VALUES (1, ?, ?, ?, ?, ?, 14, 21, ?, 'F', 1, ?, 1, ?, 1, 1, 1)
        """, (
            "COVID-19",
            "COVID-19", 
            "COVID",
            "COVID19",
            "Coronavirus Disease 2019 (COVID-19) is an infectious disease caused by SARS-CoV-2 virus. It can cause mild to severe illness and can be fatal.",
            str(uuid.uuid4()),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        print("   ✅ COVID-19 disease configured")
        
        # 2. Clear and recreate symptoms with proper web interface fields
        print("2. Setting up comprehensive symptom list...")
        cursor.execute("DELETE FROM disease_symptom WHERE disease_id = 1")
        
        symptoms_data = [
            ("Fever", "High body temperature above 38°C (100.4°F)", "Common"),
            ("Dry cough", "Persistent cough without phlegm", "Common"),
            ("Fatigue", "Extreme tiredness and lack of energy", "Common"),
            ("Loss of taste", "Ageusia - inability to taste", "Common"),
            ("Loss of smell", "Anosmia - inability to smell", "Common"),
            ("Sore throat", "Pain or irritation in the throat", "Common"),
            ("Headache", "Pain in the head or upper neck", "Common"),
            ("Aches and pains", "Muscle and joint pain", "Common"),
            ("Diarrhea", "Loose or watery bowel movements", "Less common"),
            ("Rash", "Skin irritation or discoloration", "Less common"),
            ("Discoloration of fingers", "Bluish discoloration of extremities", "Rare"),
            ("Red or irritated eyes", "Conjunctivitis", "Less common"),
            ("Difficulty breathing", "Shortness of breath at rest", "Serious"),
            ("Shortness of breath", "Difficulty breathing during activity", "Serious"),
            ("Loss of speech", "Inability to speak clearly", "Serious"),
            ("Loss of mobility", "Difficulty moving", "Serious"),
            ("Confusion", "Mental confusion or disorientation", "Serious"),
            ("Chest pain", "Pain or pressure in the chest", "Serious"),
            ("Nausea", "Feeling of sickness", "Less common"),
            ("Vomiting", "Throwing up", "Less common")
        ]
        
        symptom_id = 1
        for name, description, assessment in symptoms_data:
            cursor.execute("""
                INSERT INTO disease_symptom 
                (id, disease_id, name, description, assessment, uuid, deleted, 
                 created_by, created_on, modified_by, modified_on, 
                 approved_by, owned_by_user, realm_entity)
                VALUES (?, 1, ?, ?, ?, ?, 'F', 1, ?, 1, ?, 1, 1, 1)
            """, (
                symptom_id, name, description, assessment, str(uuid.uuid4()),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
            symptom_id += 1
        
        print(f"   ✅ {len(symptoms_data)} symptoms configured")
        
        # 3. Set up testing devices with proper fields
        print("3. Setting up testing devices...")
        cursor.execute("DELETE FROM disease_testing_device WHERE disease_id = 1")
        
        testing_devices = [
            ("RT-PCR Test", "PCR01", "Molecular", "T", "T", "Laboratory", "Gold standard molecular test"),
            ("Rapid Antigen Test", "RAT01", "Antigen", "T", "T", "Point of Care", "Quick antigen detection"),
            ("Antibody Test", "AB01", "Serological", "T", "T", "Laboratory", "Detects antibodies"),
            ("Saliva Test", "SAL01", "Molecular", "T", "T", "Point of Care", "Non-invasive collection"),
            ("Home Test Kit", "HTK01", "Antigen", "T", "T", "Home Use", "Self-administered test"),
            ("Molecular Test", "MOL01", "Molecular", "T", "T", "Laboratory", "Advanced molecular testing")
        ]
        
        device_id = 1
        for name, code, device_class, approved, available, source, comments in testing_devices:
            cursor.execute("""
                INSERT INTO disease_testing_device 
                (id, disease_id, name, code, device_class, approved, available, source, comments,
                 uuid, deleted, created_by, created_on, modified_by, modified_on,
                 approved_by, owned_by_user, realm_entity)
                VALUES (?, 1, ?, ?, ?, ?, ?, ?, ?, ?, 'F', 1, ?, 1, ?, 1, 1, 1)
            """, (
                device_id, name, code, device_class, approved, available, source, comments,
                str(uuid.uuid4()), datetime.now().isoformat(), datetime.now().isoformat()
            ))
            device_id += 1
        
        print(f"   ✅ {len(testing_devices)} testing devices configured")
        
        # 4. Demographics with proper structure
        print("4. Setting up demographics...")
        cursor.execute("DELETE FROM disease_demographic")
        
        demographics = [
            ("AG0009", "Age 0-9", "Children under 10"),
            ("AG1019", "Age 10-19", "Adolescents 10-19"),
            ("AG2029", "Age 20-29", "Young adults 20-29"),
            ("AG3039", "Age 30-39", "Adults 30-39"),
            ("AG4049", "Age 40-49", "Adults 40-49"),
            ("AG5059", "Age 50-59", "Adults 50-59"),
            ("AG6069", "Age 60-69", "Older adults 60-69"),
            ("AG7079", "Age 70-79", "Elderly 70-79"),
            ("AG80UP", "Age 80+", "Very elderly 80+"),
            ("MALE", "Male", "Male gender"),
            ("FEMALE", "Female", "Female gender"),
            ("HCW", "Healthcare Worker", "Healthcare professionals"),
            ("ESW", "Essential Worker", "Essential service workers"),
            ("IMMUNO", "Immunocompromised", "Immunocompromised individuals")
        ]
        
        demo_id = 1
        for code, name, comments in demographics:
            cursor.execute("""
                INSERT INTO disease_demographic 
                (id, code, name, comments, obsolete, uuid, deleted,
                 created_by, created_on, modified_by, modified_on,
                 approved_by, owned_by_user, realm_entity)
                VALUES (?, ?, ?, ?, 'F', ?, 'F', 1, ?, 1, ?, 1, 1, 1)
            """, (
                demo_id, code, name, comments, str(uuid.uuid4()),
                datetime.now().isoformat(), datetime.now().isoformat()
            ))
            demo_id += 1
        
        print(f"   ✅ {len(demographics)} demographic categories configured")
        
        # 5. Create comprehensive case data
        print("5. Creating comprehensive COVID-19 cases...")
        cursor.execute("DELETE FROM disease_case WHERE disease_id = 1")
        
        # Get existing persons or create new ones
        cursor.execute("SELECT id FROM pr_person WHERE deleted = 'F' OR deleted IS NULL LIMIT 25")
        person_ids = [row[0] for row in cursor.fetchall()]
        
        if len(person_ids) < 25:
            print("   Creating additional person records...")
            sample_names = [
                ("John", "Smith"), ("Jane", "Doe"), ("Mike", "Johnson"), ("Sarah", "Brown"),
                ("David", "Wilson"), ("Lisa", "Davis"), ("Chris", "Miller"), ("Emma", "Garcia"),
                ("Ryan", "Martinez"), ("Anna", "Anderson"), ("Kevin", "Taylor"), ("Maria", "Lopez"),
                ("Tom", "White"), ("Jenny", "Lee"), ("Paul", "Clark"), ("Amy", "Hall"),
                ("Mark", "Allen"), ("Kate", "Young"), ("Steve", "King"), ("Linda", "Wright"),
                ("James", "Scott"), ("Susan", "Green"), ("Bob", "Adams"), ("Helen", "Baker"),
                ("Alex", "Nelson")
            ]
            
            for i in range(25 - len(person_ids)):
                first_name, last_name = sample_names[i % len(sample_names)]
                cursor.execute("""
                    INSERT INTO pr_person 
                    (first_name, last_name, uuid, deleted, created_by, created_on, modified_by, modified_on,
                     owned_by_user, realm_entity)
                    VALUES (?, ?, ?, 'F', 1, ?, 1, ?, 1, 1)
                """, (
                    first_name, last_name, str(uuid.uuid4()), 
                    datetime.now().isoformat(), datetime.now().isoformat()
                ))
                person_ids.append(cursor.lastrowid)
        
        # Get some location IDs for cases
        cursor.execute("SELECT id FROM gis_location WHERE deleted = 'F' OR deleted IS NULL LIMIT 10")
        location_ids = [row[0] for row in cursor.fetchall()]
        if not location_ids:
            location_ids = [None] * 25
        
        illness_statuses = ["Symptomatic", "Asymptomatic", "Recovered", "Deceased"]
        diagnosis_statuses = ["Confirmed", "Probable", "Suspected", "Under Investigation"]
        monitoring_levels = ["Self-monitoring", "Active monitoring", "Direct observation", "Hospitalized"]
        
        case_id = 1
        for i in range(25):
            # Random date in the last year
            start_date = datetime.now() - timedelta(days=365)
            random_days = random.randint(0, 365)
            case_date = start_date + timedelta(days=random_days)
            symptom_date = case_date - timedelta(days=random.randint(0, 14))
            
            illness_status = random.choice(illness_statuses)
            diagnosis_status = random.choice(diagnosis_statuses)
            monitoring_level = random.choice(monitoring_levels)
            hospitalized = 'T' if random.random() < 0.3 else 'F'
            intensive_care = 'T' if hospitalized == 'T' and random.random() < 0.2 else 'F'
            
            case_number = f"COVID-{datetime.now().year}-{i+1:04d}"
            person_id = person_ids[i % len(person_ids)]
            location_id = location_ids[i % len(location_ids)] if location_ids[0] else None
            
            cursor.execute("""
                INSERT INTO disease_case 
                (id, case_number, person_id, disease_id, location_id, illness_status,
                 symptom_debut, hospitalized, intensive_care, diagnosis_status, diagnosis_date,
                 monitoring_level, uuid, deleted, created_by, created_on, modified_by, modified_on,
                 approved_by, owned_by_user, realm_entity)
                VALUES (?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'F', 1, ?, 1, ?, 1, 1, 1)
            """, (
                case_id, case_number, person_id, location_id, illness_status,
                symptom_date.date().isoformat(), hospitalized, intensive_care,
                diagnosis_status, case_date.date().isoformat(), monitoring_level,
                str(uuid.uuid4()), datetime.now().isoformat(), datetime.now().isoformat()
            ))
            case_id += 1
        
        print(f"   ✅ 25 comprehensive cases created")
        
        # 6. Testing reports with better structure
        print("6. Creating testing reports...")
        cursor.execute("DELETE FROM disease_testing_report WHERE disease_id = 1")
        
        report_id = 1
        for i in range(50):
            test_date = datetime.now() - timedelta(days=random.randint(0, 365))
            tests_total = random.randint(50, 1000)
            tests_positive = random.randint(0, int(tests_total * 0.25))  # Max 25% positive
            
            # Get a random site/location
            site_id = location_ids[i % len(location_ids)] if location_ids[0] else None
            
            cursor.execute("""
                INSERT INTO disease_testing_report 
                (id, disease_id, site_id, date, tests_total, tests_positive,
                 comments, uuid, deleted, created_by, created_on, modified_by, modified_on,
                 approved_by, owned_by_user, realm_entity)
                VALUES (?, 1, ?, ?, ?, ?, ?, ?, 'F', 1, ?, 1, ?, 1, 1, 1)
            """, (
                report_id, site_id, test_date.date().isoformat(), tests_total, tests_positive,
                f"Daily testing report for {test_date.strftime('%Y-%m-%d')}",
                str(uuid.uuid4()), datetime.now().isoformat(), datetime.now().isoformat()
            ))
            report_id += 1
        
        print(f"   ✅ 50 testing reports created")
        
        conn.commit()
        conn.close()
        
        print("\n🎉 COMPREHENSIVE COVID-19 DATABASE SETUP COMPLETED!")
        print("=" * 60)
        print("📊 SUMMARY:")
        print("   • 1 Disease (COVID-19) with full configuration")
        print("   • 20 Symptoms with descriptions and severity levels")
        print("   • 6 Testing devices with approval status")
        print("   • 14 Demographic categories")
        print("   • 25 Cases with person and location links")
        print("   • 50 Testing reports with site data")
        print("\n🌐 WEB INTERFACE ACCESS:")
        print("   • Main Disease Page: http://127.0.0.1:8000/eden/disease")
        print("   • Cases Management: http://127.0.0.1:8000/eden/disease/case")
        print("   • Statistics: http://127.0.0.1:8000/eden/disease/stats_data")
        print("   • Admin Panel: http://127.0.0.1:8000/admin")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating comprehensive data: {e}")
        return False

if __name__ == "__main__":
    create_comprehensive_covid_data()
