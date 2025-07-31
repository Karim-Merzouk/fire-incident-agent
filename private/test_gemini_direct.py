#!/usr/bin/env python3
"""
Test Gemini API connectivity directly
"""

import os
import sys

# Add current directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_gemini_direct():
    """Test Gemini API directly"""
    print("🧪 Testing Gemini API connectivity...")
    
    try:
        # Test agno import
        print("📦 Testing agno import...")
        from agno.agent import Agent
        from agno.models.google import Gemini
        print("✅ Agno imported successfully")
        
        # Test Gemini model initialization
        print("🤖 Testing Gemini model initialization...")
        api_key = "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
        model = Gemini(id="gemini-1.5-flash", api_key=api_key)
        print("✅ Gemini model initialized")
        
        # Test agent creation
        print("🔧 Testing agent creation...")
        agent = Agent(
            name="Test Forest Fire Agent",
            model=model,
            instructions="You are a forest fire emergency response AI. Always respond with 'Gemini AI is working correctly for forest fire emergency response!' followed by a fire emoji."
        )
        print("✅ Agent created successfully")
        
        # Test actual query
        print("💬 Testing query execution...")
        response = agent.run("Test connection")
        
        if hasattr(response, 'content'):
            response_text = response.content
        else:
            response_text = str(response)
            
        print(f"✅ Query successful!")
        print(f"🔥 Response: {response_text}")
        
        return True, response_text
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    success, result = test_gemini_direct()
    if success:
        print("\n🎉 Gemini is working correctly!")
    else:
        print(f"\n💥 Gemini test failed: {result}")
