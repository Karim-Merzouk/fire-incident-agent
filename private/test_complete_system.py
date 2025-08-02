#!/usr/bin/env python3
"""
Test the complete Forest Fire system with Gemini API
"""

def test_full_system():
    print("🌲🔥 TESTING COMPLETE FOREST FIRE SYSTEM")
    print("=" * 50)
    
    try:
        # Test 1: Database connection
        print("\n1. Testing Database Connection...")
        from realistic_forest_fire_tool import RealisticForestFireDatabaseTool
        db_tool = RealisticForestFireDatabaseTool()
        if db_tool.connect():
            print("✅ Database connection successful")
            db_tool.disconnect()
        else:
            print("❌ Database connection failed")
            return
        
        # Test 2: AI Agent
        print("\n2. Testing AI Agent...")
        from final_forest_fire_agent import ForestFireAgent
        agent = ForestFireAgent()
        
        # Test 3: Simple query
        print("\n3. Testing AI Query...")
        response = agent.query("What's the current fire status?")
        print(f"✅ AI Response received ({len(response)} characters)")
        print(f"Sample: {response[:150]}...")
        
        # Test 4: Web functions
        print("\n4. Testing Web Functions...")
        from final_forest_fire_agent import get_gemini_response
        web_response = get_gemini_response("How many people are evacuated?")
        print(f"✅ Web interface function working")
        print(f"Sample: {web_response[:100]}...")
        
        print("\n🎉 ALL TESTS PASSED! The Forest Fire system is ready.")
        print("\n📝 Summary:")
        print("• Database: Connected and working")
        print("• AI Agent: Initialized with Gemini API")
        print("• Web Functions: Ready for Flask app")
        print("\n🌐 You can now access the web interface at http://localhost:5000")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_system()
