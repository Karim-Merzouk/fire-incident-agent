"""
COVID-19 Database Agent Demo
Test the database connectivity and basic functionality
"""

from covid_database_tool import COVID19DatabaseTool
import json

def test_database_tool():
    """Test the database tool functionality"""
    print("🔍 COVID-19 Database Tool Test")
    print("=" * 50)
    
    # Initialize the tool
    tool = COVID19DatabaseTool()
    
    try:
        # Test 1: Database Overview
        print("\n📊 DATABASE OVERVIEW:")
        overview = tool.get_covid_overview()
        print(json.dumps(overview, indent=2))
        
        # Test 2: Recent Cases
        print("\n🏥 RECENT CASES (Top 5):")
        recent_cases = tool.get_recent_cases(5)
        for i, case in enumerate(recent_cases, 1):
            hosp_status = "🏥 Hospitalized" if case.get('hospitalized') == 'T' else "🏠 Home"
            icu_status = " (ICU)" if case.get('intensive_care') == 'T' else ""
            print(f"{i}. {case.get('case_number')}: {case.get('illness_status')} | {case.get('diagnosis_status')}")
            print(f"   📅 {case.get('diagnosis_date')} | {hosp_status}{icu_status}")
        
        # Test 3: Symptoms
        print("\n🤒 COVID-19 SYMPTOMS:")
        symptoms = tool.get_symptoms_list()
        for symptom in symptoms[:10]:  # Show first 10
            severity = symptom.get('assessment', 'Unknown')
            print(f"• {symptom.get('name')} ({severity})")
            if symptom.get('description'):
                print(f"  {symptom.get('description')}")
        
        # Test 4: Testing Devices
        print("\n🔬 TESTING DEVICES:")
        devices = tool.get_testing_devices()
        for device in devices:
            status = "✅ Approved" if device.get('approved') == 'T' else "⏳ Pending"
            available = "📦 Available" if device.get('available') == 'T' else "❌ Unavailable"
            print(f"• {device.get('name')} ({device.get('code')})")
            print(f"  Class: {device.get('device_class')} | {status} | {available}")
        
        # Test 5: Testing Statistics
        print("\n📈 RECENT TESTING STATISTICS (Last 10 reports):")
        test_stats = tool.get_testing_statistics(30)
        for stat in test_stats[:10]:
            date = stat.get('date')
            total = stat.get('tests_total', 0)
            positive = stat.get('tests_positive', 0)
            rate = stat.get('positivity_rate', 0)
            print(f"📅 {date}: {total:3d} tests, {positive:2d} positive ({rate:.1f}%)")
        
        # Test 6: Hospitalization Trends
        print("\n🏥 HOSPITALIZATION TRENDS:")
        trends = tool.get_hospitalization_trends()
        if 'trends' in trends:
            for trend in trends['trends'][:6]:  # Show last 6 months
                month = trend.get('month')
                total = trend.get('total_cases', 0)
                hosp = trend.get('hospitalized', 0)
                icu = trend.get('icu', 0)
                hosp_rate = trend.get('hospitalization_rate', 0)
                print(f"📅 {month}: {total} cases, {hosp} hospitalized ({hosp_rate:.1f}%), {icu} ICU")
        
        print("\n✅ Database tool test completed successfully!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def interactive_demo():
    """Interactive demo of database queries"""
    print("\n🎯 INTERACTIVE DATABASE DEMO")
    print("=" * 50)
    
    tool = COVID19DatabaseTool()
    
    print("Available commands:")
    print("1. overview - Get database overview")
    print("2. cases [number] - Get recent cases (default 10)")
    print("3. symptoms - List all symptoms")
    print("4. devices - List testing devices")
    print("5. stats [days] - Get testing statistics (default 30 days)")
    print("6. status [status] - Search cases by status")
    print("7. custom [sql] - Execute custom SELECT query")
    print("8. quit - Exit demo")
    
    while True:
        try:
            command = input("\n💬 Enter command: ").strip().lower()
            
            if command == "quit" or command == "q":
                break
            elif command == "overview":
                result = tool.get_covid_overview()
                print(json.dumps(result, indent=2))
            elif command.startswith("cases"):
                parts = command.split()
                limit = int(parts[1]) if len(parts) > 1 else 10
                result = tool.get_recent_cases(limit)
                for case in result:
                    print(f"• {case.get('case_number')}: {case.get('illness_status')} ({case.get('diagnosis_date')})")
            elif command == "symptoms":
                result = tool.get_symptoms_list()
                for symptom in result:
                    print(f"• {symptom.get('name')}: {symptom.get('description', 'No description')}")
            elif command == "devices":
                result = tool.get_testing_devices()
                for device in result:
                    print(f"• {device.get('name')} ({device.get('code')}): {device.get('device_class')}")
            elif command.startswith("stats"):
                parts = command.split()
                days = int(parts[1]) if len(parts) > 1 else 30
                result = tool.get_testing_statistics(days)
                for stat in result[:15]:  # Limit to 15 results
                    print(f"• {stat.get('date')}: {stat.get('tests_total')} tests, {stat.get('positivity_rate')}% positive")
            elif command.startswith("status"):
                parts = command.split(maxsplit=1)
                if len(parts) < 2:
                    print("❌ Please specify a status to search for")
                    continue
                status = parts[1]
                result = tool.search_cases_by_status(status)
                for case in result[:10]:  # Limit to 10 results
                    print(f"• {case.get('case_number')}: {case.get('illness_status')} | {case.get('diagnosis_status')}")
            elif command.startswith("custom"):
                parts = command.split(maxsplit=1)
                if len(parts) < 2:
                    print("❌ Please specify a SQL query")
                    continue
                query = parts[1]
                result = tool.custom_query(query)
                if result and 'error' not in result[0]:
                    for row in result[:10]:  # Limit to 10 results
                        print(f"• {row}")
                else:
                    print(f"❌ Query error: {result}")
            else:
                print("❌ Unknown command. Type 'quit' to exit.")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("👋 Demo ended!")

if __name__ == "__main__":
    # Run the database test
    success = test_database_tool()
    
    if success:
        # Ask if user wants interactive demo
        response = input("\n🎯 Would you like to try the interactive demo? (y/n): ")
        if response.lower().startswith('y'):
            interactive_demo()
    else:
        print("❌ Database test failed. Please check your database setup.")
        
    print("\n🚀 Next steps:")
    print("1. Set up your AI API key in .env file (copy from .env.example)")
    print("2. Run: python covid_agent.py")
    print("3. Start asking questions about your COVID-19 data!")
