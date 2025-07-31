#!/usr/bin/env python3
"""
🌲🔥 FOREST FIRE EMERGENCY WEB INTERFACE - STARTUP SCRIPT
========================================================

Quick startup script for the Forest Fire Emergency Web Interface.
This script launches the Flask web application with proper configuration.
"""

import os
import sys
import webbrowser
from datetime import datetime

def main():
    print("🌲🔥 FOREST FIRE EMERGENCY WEB INTERFACE")
    print("=" * 60)
    print(f"📅 Starting at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check if we're in the right directory
    current_dir = os.getcwd()
    if not os.path.exists("forest_fire_web_app.py"):
        print("❌ Error: forest_fire_web_app.py not found!")
        print(f"Current directory: {current_dir}")
        print("Please run this script from the private directory.")
        return 1
    
    print("🔍 Checking system components...")
    
    # Check database
    db_path = "../databases/storage.db"
    if os.path.exists(db_path):
        print("✅ Database found")
    else:
        print("⚠️ Database not found - will use fallback data")
    
    # Check AI components
    try:
        from realistic_forest_fire_tool import ForestFireEmergencyDatabase
        print("✅ Database tools available")
    except ImportError:
        print("⚠️ Database tools not available - will use fallback")
    
    try:
        from final_forest_fire_agent import ForestFireAgent
        print("✅ AI agent available")
    except ImportError:
        print("⚠️ AI agent not available - will use pattern matching")
    
    # Check .env file
    if os.path.exists(".env"):
        print("✅ Configuration file found")
    else:
        print("⚠️ .env file not found - AI features may be limited")
    
    print()
    print("🚀 Starting web server...")
    print("📱 Web Interface URLs:")
    print("   Dashboard: http://localhost:5000/")
    print("   AI Chat:   http://localhost:5000/chat")
    print("   API Data:  http://localhost:5000/api/overview")
    print()
    print("💡 The web interface will open automatically in your browser.")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Auto-open browser after a short delay
    import threading
    def open_browser():
        import time
        time.sleep(2)  # Wait for server to start
        try:
            webbrowser.open('http://localhost:5000/')
            print("🌐 Opened web interface in your default browser")
        except Exception as e:
            print(f"⚠️ Could not auto-open browser: {e}")
            print("   Please manually open: http://localhost:5000/")
    
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Import and run the Flask app
    try:
        from forest_fire_web_app import app
        app.run(debug=True, host='0.0.0.0', port=5000, use_reloader=False)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return 0
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
