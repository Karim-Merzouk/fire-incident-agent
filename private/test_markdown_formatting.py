#!/usr/bin/env python3
"""
Test Markdown formatting in Forest Fire system
"""

def test_markdown_formatting():
    print("📝 TESTING MARKDOWN FORMATTING")
    print("=" * 40)
    
    from final_forest_fire_agent import ForestFireAgent, get_gemini_response
    
    # Test 1: Direct agent query
    print("\n1. Testing Agent Markdown Output...")
    agent = ForestFireAgent()
    response = agent.query("Give me a well-formatted markdown report on current fire status")
    
    # Check for markdown elements
    markdown_elements = {
        'headers': '##' in response or '###' in response,
        'bold': '**' in response,
        'bullet_points': '* ' in response or '- ' in response,
        'emphasis': '*' in response and '**' not in response.replace('**', ''),
    }
    
    print(f"✅ Contains headers: {markdown_elements['headers']}")
    print(f"✅ Contains bold text: {markdown_elements['bold']}")
    print(f"✅ Contains bullet points: {markdown_elements['bullet_points']}")
    print(f"✅ Contains emphasis: {markdown_elements['emphasis']}")
    
    # Test 2: Web interface function
    print("\n2. Testing Web Interface Markdown...")
    web_response = get_gemini_response("Format evacuation status as markdown")
    
    web_markdown_elements = {
        'headers': '##' in web_response or '###' in web_response,
        'bold': '**' in web_response,
        'structure': '###' in web_response and '**' in web_response,
    }
    
    print(f"✅ Web response has headers: {web_markdown_elements['headers']}")
    print(f"✅ Web response has bold: {web_markdown_elements['bold']}")
    print(f"✅ Web response is well structured: {web_markdown_elements['structure']}")
    
    # Test 3: Show sample output
    print("\n3. Sample Markdown Output:")
    print("-" * 40)
    print(response[:300] + "...")
    print("-" * 40)
    
    if all(markdown_elements.values()):
        print("\n🎉 All Markdown elements are present!")
        print("The web interface should now display properly formatted responses.")
    else:
        print("\n⚠️ Some Markdown elements may be missing.")
    
    print("\n📱 Test the web interface at: http://localhost:5000/chat")
    print("   Try asking: 'Give me a formatted fire status report'")

if __name__ == "__main__":
    test_markdown_formatting()
