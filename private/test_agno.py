#!/usr/bin/env python3
"""
Test Agno framework
"""

def test_agno():
    try:
        print("Testing agno import...")
        from agno.agent import Agent
        from agno.models.google import Gemini
        print("✅ Agno import successful")
        
        print("Testing model creation...")
        model = Gemini(id="gemini-1.5-flash", api_key="AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI")
        print("✅ Gemini model created")
        
        print("Testing agent creation...")
        agent = Agent(
            name="Test Forest Fire Agent",
            model=model,
            instructions="You are a forest fire emergency AI. Respond with 'Agno Gemini is working!'"
        )
        print("✅ Agent created")
        
        print("Testing query...")
        response = agent.run("Test connection")
        print(f"✅ Response: {response}")
        
        return True
    except Exception as e:
        print(f"❌ Agno Error: {e}")
        return False

if __name__ == "__main__":
    test_agno()
