#!/usr/bin/env python3
"""
Test Google Generative AI directly without agno
"""

import os

def test_google_gemini():
    """Test Google Generative AI directly"""
    print("🧪 Testing Google Generative AI (Gemini) directly...")
    
    try:
        # Test google.generativeai import
        print("📦 Testing google.generativeai import...")
        import google.generativeai as genai
        print("✅ Google Generative AI imported successfully")
        
        # Configure API
        print("🔑 Configuring API key...")
        api_key = "AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI"
        genai.configure(api_key=api_key)
        print("✅ API configured")
        
        # Create model
        print("🤖 Creating Gemini model...")
        model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Model created")
        
        # Test generation
        print("💬 Testing content generation...")
        response = model.generate_content("You are a forest fire emergency AI. Say 'Gemini is working!' and include a fire emoji.")
        print(f"✅ Generation successful!")
        print(f"🔥 Response: {response.text}")
        
        return True, response.text
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False, str(e)

if __name__ == "__main__":
    success, result = test_google_gemini()
    if success:
        print("\n🎉 Google Generative AI (Gemini) is working correctly!")
    else:
        print(f"\n💥 Test failed: {result}")
