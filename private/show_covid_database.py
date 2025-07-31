import sqlite3
import os

def show_covid_database():
    db_path = os.path.join(os.path.dirname(__file__), "..", "databases", "storage.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🦠 SAHANA EDEN COVID-19 DATABASE")
        print("=" * 60)
        
        # 1. Disease Information
        print("\n📋 DISEASE INFORMATION:")
        print("-" * 40)
        cursor.execute("SELECT name, description FROM disease_disease WHERE id = 1")
        disease = cursor.fetchone()
        if disease:
            print(f"Disease: {disease[0]}")
            print(f"Description: {disease[1]}")
        
        # 2. Symptoms
        print("\n🤒 COVID-19 SYMPTOMS:")
        print("-" * 40)
        cursor.execute("SELECT name FROM disease_symptom WHERE disease_id = 1 ORDER BY name")
        symptoms = cursor.fetchall()
        for i, symptom in enumerate(symptoms, 1):
            print(f"{i:2d}. {symptom[0]}")
        
        # 3. Testing Devices
        print("\n🔬 TESTING DEVICES:")
        print("-" * 40)
        cursor.execute("SELECT name, code, device_class, approved, available FROM disease_testing_device WHERE disease_id = 1")
        devices = cursor.fetchall()
        for device in devices:
            status = "✅ Approved" if device[3] == 'T' else "⏳ Pending"
            availability = "📦 Available" if device[4] == 'T' else "❌ Unavailable"
            print(f"• {device[0]} ({device[1]})")
            print(f"  Class: {device[2]} | {status} | {availability}")
        
        # 4. Demographics
        print("\n👥 DEMOGRAPHIC CATEGORIES:")
        print("-" * 40)
        cursor.execute("SELECT code, name FROM disease_demographic ORDER BY code")
        demographics = cursor.fetchall()
        for demo in demographics:
            print(f"• {demo[0]}: {demo[1]}")
        
        # 5. Cases Summary
        print("\n🏥 COVID-19 CASES SUMMARY:")
        print("-" * 40)
        cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1")
        total_cases = cursor.fetchone()[0]
        print(f"Total Cases: {total_cases}")
        
        # Cases by status
        cursor.execute("""
            SELECT illness_status, COUNT(*) 
            FROM disease_case 
            WHERE disease_id = 1 
            GROUP BY illness_status 
            ORDER BY COUNT(*) DESC
        """)
        status_counts = cursor.fetchall()
        for status, count in status_counts:
            print(f"  {status}: {count} cases")
        
        # Cases by diagnosis status
        print("\n📊 DIAGNOSIS STATUS:")
        cursor.execute("""
            SELECT diagnosis_status, COUNT(*) 
            FROM disease_case 
            WHERE disease_id = 1 
            GROUP BY diagnosis_status 
            ORDER BY COUNT(*) DESC
        """)
        diagnosis_counts = cursor.fetchall()
        for diagnosis, count in diagnosis_counts:
            print(f"  {diagnosis}: {count} cases")
        
        # Hospitalization stats
        cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1 AND hospitalized = 'T'")
        hospitalized = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM disease_case WHERE disease_id = 1 AND intensive_care = 'T'")
        icu = cursor.fetchone()[0]
        print(f"\n🏥 Hospitalized: {hospitalized} cases")
        print(f"🚨 ICU: {icu} cases")
        
        # 6. Testing Reports Summary
        print("\n📊 TESTING REPORTS SUMMARY:")
        print("-" * 40)
        cursor.execute("SELECT COUNT(*) FROM disease_testing_report WHERE disease_id = 1")
        total_reports = cursor.fetchone()[0]
        cursor.execute("SELECT SUM(tests_total) FROM disease_testing_report WHERE disease_id = 1")
        total_tests = cursor.fetchone()[0] or 0
        cursor.execute("SELECT SUM(tests_positive) FROM disease_testing_report WHERE disease_id = 1")
        total_positive = cursor.fetchone()[0] or 0
        
        print(f"Testing Reports: {total_reports}")
        print(f"Total Tests Conducted: {total_tests:,}")
        print(f"Total Positive Tests: {total_positive:,}")
        if total_tests > 0:
            positivity_rate = (total_positive / total_tests) * 100
            print(f"Positivity Rate: {positivity_rate:.1f}%")
        
        # Recent test reports
        print("\n📅 RECENT TEST REPORTS (Last 10):")
        cursor.execute("""
            SELECT date, tests_total, tests_positive 
            FROM disease_testing_report 
            WHERE disease_id = 1 
            ORDER BY date DESC 
            LIMIT 10
        """)
        recent_reports = cursor.fetchall()
        for report in recent_reports:
            date, total, positive = report
            rate = (positive / total * 100) if total > 0 else 0
            print(f"  {date}: {total:3d} tests, {positive:2d} positive ({rate:.1f}%)")
        
        # 7. Sample Cases Details
        print("\n📋 SAMPLE CASES (First 10):")
        print("-" * 40)
        cursor.execute("""
            SELECT case_number, illness_status, diagnosis_status, diagnosis_date, 
                   hospitalized, intensive_care, monitoring_level
            FROM disease_case 
            WHERE disease_id = 1 
            ORDER BY diagnosis_date DESC 
            LIMIT 10
        """)
        cases = cursor.fetchall()
        for case in cases:
            case_num, illness, diagnosis, date, hosp, icu, monitoring = case
            hosp_status = "🏥" if hosp == 'T' else "🏠"
            icu_status = "🚨" if icu == 'T' else ""
            print(f"  {case_num}: {illness} | {diagnosis} | {date} {hosp_status}{icu_status}")
            print(f"    Monitoring: {monitoring}")
        
        print("\n" + "=" * 60)
        print("🎯 DATABASE ACCESS METHODS:")
        print("  • Web Interface: http://127.0.0.1:8000/eden/disease")
        print("  • Admin Panel: http://127.0.0.1:8000/admin")
        print("  • Database File: applications/eden/databases/storage.db")
        print("=" * 60)
        
        conn.close()
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    show_covid_database()
