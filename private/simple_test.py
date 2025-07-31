#!/usr/bin/env python3
"""
Simple Google AI test
"""

def simple_google_test():
    try:
        print("Testing basic import...")
        import google.generativeai as genai
        print("✅ Import successful")
        
        print("Testing configuration...")
        genai.configure(api_key="AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI")
        print("✅ Configuration successful")
        
        print("Testing model creation...")
        model = genai.GenerativeModel('gemini-pro')
        print("✅ Model creation successful")
        
        print("Testing generation...")
        response = model.generate_content("Hello! Just say 'Working!'")
        print(f"✅ Response: {response.text}")
        
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    simple_google_test()
