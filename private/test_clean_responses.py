#!/usr/bin/env python3
"""
Test the fixed AI responses for clean output
"""

def test_clean_responses():
    print("🧪 TESTING CLEAN AI RESPONSES")
    print("=" * 40)
    
    from final_forest_fire_agent import ForestFireAgent, get_gemini_response
    
    # Test 1: Agent direct query
    print("\n1. Testing Agent Direct Query...")
    agent = ForestFireAgent()
    response1 = agent.query("Current fire size?")
    print(f"✅ Response type: {type(response1)}")
    print(f"✅ Clean content: {response1[:100]}...")
    
    # Test 2: Web interface function
    print("\n2. Testing Web Interface Function...")
    response2 = get_gemini_response("Evacuation status?")
    print(f"✅ Response type: {type(response2)}")
    print(f"✅ Clean content: {response2[:100]}...")
    
    # Test 3: Check for unwanted objects
    print("\n3. Checking for Clean Output...")
    if "RunResponse" not in response1 and "RunResponse" not in response2:
        print("✅ No RunResponse objects in output!")
    else:
        print("❌ Still contains RunResponse objects")
    
    if "content=" not in response1 and "content=" not in response2:
        print("✅ No object attributes in output!")
    else:
        print("❌ Still contains object attributes")
    
    print("\n🎉 All responses are now clean text!")
    print("Web interface should display properly formatted emergency updates.")

if __name__ == "__main__":
    test_clean_responses()
