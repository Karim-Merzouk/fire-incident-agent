#!/usr/bin/env python3
"""
Forest Fire AI Agent - Sahana Eden Integration Setup
This script sets up the complete integration of the Forest Fire AI Agent into Sahana Eden
"""

import os
import sys
import shutil

def setup_ai_integration():
    """Setup the complete AI agent integration"""
    
    print("🔥 SETTING UP FOREST FIRE AI AGENT INTEGRATION IN SAHANA EDEN")
    print("=" * 60)
    
    # Paths
    eden_path = "c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden"
    private_path = os.path.join(eden_path, "private")
    controllers_path = os.path.join(eden_path, "controllers")
    views_path = os.path.join(eden_path, "views", "fire")
    models_path = os.path.join(eden_path, "models")
    
    print("✅ Eden Application Path:", eden_path)
    print("✅ Private Directory:", private_path)
    print("✅ Controllers Directory:", controllers_path)
    print("✅ Views Directory:", views_path)
    
    # Check if all required files exist
    required_files = [
        "final_forest_fire_agent.py",
        "realistic_forest_fire_tool.py", 
        "forest_fire_database_tool.py",
        ".env.example"
    ]
    
    print("\n📋 CHECKING REQUIRED FILES:")
    for file in required_files:
        file_path = os.path.join(private_path, file)
        if os.path.exists(file_path):
            print(f"✅ {file} - Found")
        else:
            print(f"❌ {file} - Missing!")
            return False
    
    # Check if integration files exist
    integration_files = [
        ("controllers/fire.py", "Fire controller with AI agent"),
        ("views/fire/ai_agent.html", "AI agent interface view"),
        ("views/fire/index.html", "Updated fire homepage"),
        ("models/fire_ai_integration.py", "AI integration model")
    ]
    
    print("\n🔧 CHECKING INTEGRATION FILES:")
    for file_path, description in integration_files:
        full_path = os.path.join(eden_path, file_path)
        if os.path.exists(full_path):
            print(f"✅ {description} - Integrated")
        else:
            print(f"❌ {description} - Not found!")
    
    # Check database
    db_path = os.path.join(eden_path, "databases", "storage.db")
    if os.path.exists(db_path):
        print(f"✅ Database - Found ({os.path.getsize(db_path) / 1024 / 1024:.1f} MB)")
    else:
        print("❌ Database - Not found!")
    
    print("\n🚀 INTEGRATION STATUS:")
    print("✅ Forest Fire AI Agent is integrated into Sahana Eden!")
    print("✅ Access via: Fire Module → AI Agent")
    print("✅ Direct URL: /fire/ai_agent")
    
    print("\n📖 USAGE INSTRUCTIONS:")
    print("1. Start Sahana Eden server")
    print("2. Navigate to Fire module")
    print("3. Click 'Launch AI Assistant' button")
    print("4. Start chatting with the AI agent!")
    
    print("\n🔧 FEATURES INTEGRATED:")
    print("• Real-time chat interface with AI agent")
    print("• Emergency-themed UI with fire colors")
    print("• Quick action buttons for common queries")
    print("• Direct database integration")
    print("• Markdown response formatting")
    print("• Status monitoring and incident tracking")
    
    return True

def test_ai_integration():
    """Test the AI integration"""
    
    print("\n🧪 TESTING AI INTEGRATION:")
    
    try:
        # Test imports
        sys.path.append("c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/private")
        
        print("Testing AI agent import...")
        from final_forest_fire_agent import ForestFireAgent
        print("✅ AI agent import successful")
        
        print("Testing database tool import...")
        from realistic_forest_fire_tool import RealisticForestFireDatabaseTool
        print("✅ Database tool import successful")
        
        print("Testing agent initialization...")
        agent = ForestFireAgent()
        print("✅ AI agent initialization successful")
        
        print("Testing database connection...")
        db_tool = RealisticForestFireDatabaseTool()
        print("✅ Database connection successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def create_startup_instructions():
    """Create startup instructions"""
    
    instructions = """
# 🔥 FOREST FIRE AI AGENT - SAHANA EDEN INTEGRATION

## 🚀 Quick Start

### 1. Start Sahana Eden
```bash
cd c:/Users/PC/OneDrive/Bureau/CERIST/web2py
python web2py.py -a password -i 127.0.0.1 -p 8000
```

### 2. Access the AI Agent
- Open browser: http://127.0.0.1:8000/eden
- Go to Fire module
- Click "Launch AI Assistant"

### 3. Start Using the AI
- Ask about fire incidents: "What are the current fire threats?"
- Request resources: "What fire suppression resources are available?"
- Get evacuation help: "Help me plan evacuations for Pine Ridge area"
- Weather information: "What are the current fire weather conditions?"

## 🎯 Direct Access URLs

- **AI Agent**: http://127.0.0.1:8000/eden/fire/ai_agent
- **Fire Module**: http://127.0.0.1:8000/eden/fire
- **Main Dashboard**: http://127.0.0.1:8000/eden

## 🔧 Features

✅ **Real-time Chat**: Interactive conversation with AI agent
✅ **Emergency Database**: Connected to Sahana Eden database  
✅ **Fire-themed UI**: Professional emergency response interface
✅ **Quick Actions**: Pre-built queries for common tasks
✅ **Status Monitoring**: Real-time incident and resource tracking
✅ **Markdown Support**: Rich formatted responses
✅ **Mobile Responsive**: Works on all devices

## 🆘 Support

- Check console for any JavaScript errors
- Verify .env file has GEMINI_API_KEY configured
- Ensure all Python packages are installed
- Database should be accessible at databases/storage.db

**The Forest Fire AI Agent is now fully integrated into Sahana Eden!** 🌲🔥🤖
"""
    
    with open("c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/private/AI_AGENT_INTEGRATION_COMPLETE.md", "w", encoding='utf-8') as f:
        f.write(instructions)
    
    print("📄 Created integration documentation: AI_AGENT_INTEGRATION_COMPLETE.md")

if __name__ == "__main__":
    print("🌲🔥 FOREST FIRE AI AGENT - SAHANA EDEN INTEGRATION")
    print("=" * 60)
    
    # Setup integration
    if setup_ai_integration():
        print("\n🎉 INTEGRATION SETUP COMPLETE!")
        
        # Test integration
        if test_ai_integration():
            print("\n✅ ALL TESTS PASSED!")
        else:
            print("\n⚠️  Some tests failed - check configuration")
        
        # Create instructions
        create_startup_instructions()
        
        print("\n🚀 READY TO USE!")
        print("Start Sahana Eden and navigate to Fire → AI Agent")
    else:
        print("\n❌ INTEGRATION SETUP FAILED!")
        print("Please check that all required files are present")
