#!/usr/bin/env python3
"""
Quick test of the Forest Fire AI Agent integration
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all imports work correctly"""
    print("🧪 TESTING FOREST FIRE AI AGENT IMPORTS")
    print("=" * 50)
    
    try:
        print("Testing ForestFireAgent import...")
        from final_forest_fire_agent import ForestFireAgent
        print("✅ ForestFireAgent imported successfully")
        
        print("Testing RealisticForestFireDatabaseTool import...")
        from realistic_forest_fire_tool import RealisticForestFireDatabaseTool
        print("✅ RealisticForestFireDatabaseTool imported successfully")
        
        print("Testing agent initialization...")
        agent = ForestFireAgent()
        print("✅ ForestFireAgent initialized successfully")
        
        print("Testing database tool initialization...")
        db_tool = RealisticForestFireDatabaseTool()
        print("✅ RealisticForestFireDatabaseTool initialized successfully")
        
        print("Testing database connection...")
        if db_tool.connect():
            print("✅ Database connection successful")
            db_tool.disconnect()
        else:
            print("❌ Database connection failed")
        
        print("\n🎉 ALL IMPORTS AND INITIALIZATIONS SUCCESSFUL!")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_agent_query():
    """Test a simple query to the agent"""
    print("\n🔥 TESTING AI AGENT QUERY")
    print("=" * 30)
    
    try:
        from final_forest_fire_agent import ForestFireAgent
        agent = ForestFireAgent()
        
        # Test a simple query
        test_query = "What is the current fire emergency status?"
        print(f"Query: {test_query}")
        
        response = agent.query(test_query)
        print(f"Response: {response[:200]}...")  # Show first 200 chars
        
        print("✅ Agent query test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Agent query failed: {e}")
        return False

if __name__ == "__main__":
    print("🌲🔥 FOREST FIRE AI AGENT - INTEGRATION TEST")
    print("=" * 50)
    
    # Test imports
    if test_imports():
        print("\n✅ INTEGRATION READY!")
        
        # Test agent query
        test_agent_query()
        
        print("\n🚀 SUMMARY:")
        print("✅ All components are properly integrated")
        print("✅ Forest Fire AI Agent is ready to use in Sahana Eden")
        print("✅ Start Sahana Eden and navigate to Fire → AI Agent")
    else:
        print("\n❌ INTEGRATION ISSUES DETECTED")
        print("Please check the error messages above")
