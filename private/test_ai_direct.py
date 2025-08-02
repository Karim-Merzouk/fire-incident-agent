#!/usr/bin/env python3
"""
Direct test of AI components
"""

def test_imports():
    """Test all AI-related imports"""
    print("🧪 Testing AI Component Imports...")
    
    # Test 1: Google Generative AI
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
        
        # Test configuration
        api_key = "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
        genai.configure(api_key=api_key)
        print("✅ Google AI configured successfully")
        
        # Test model creation
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Gemini model created successfully")
        
        # Test simple generation
        response = model.generate_content("Say 'Hello from Gemini!'")
        print(f"✅ Gemini response: {response.text}")
        
        return True, "google_ai"
        
    except Exception as e:
        print(f"❌ Google AI failed: {e}")
    
    # Test 2: Agno Framework
    try:
        from agno.agent import Agent
        from agno.models.google import Gemini
        print("✅ Agno framework imported successfully")
        
        api_key = "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
        model = Gemini(id="gemini-1.5-flash", api_key=api_key)
        print("✅ Agno Gemini model created")
        
        agent = Agent(
            name="Test Agent",
            model=model,
            instructions="Say 'Hello from Agno!'"
        )
        print("✅ Agno agent created successfully")
        
        response = agent.run("Test")
        print(f"✅ Agno response: {response}")
        
        return True, "agno"
        
    except Exception as e:
        print(f"❌ Agno failed: {e}")
    
    return False, "fallback"

if __name__ == "__main__":
    success, mode = test_imports()
    print(f"\n🎯 Result: AI Mode = {mode}")
    print(f"🎯 Success: {success}")
