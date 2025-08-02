#!/usr/bin/env python3
"""
🌲🔥 FOREST FIRE WEB INTERFACE LAUNCHER
======================================

Quick launcher for the Forest Fire Emergency Web Interface.
This script starts the web server and opens the interface in your browser.
"""

import subprocess
import webbrowser
import time
import threading
import sys
import os

def open_browser_after_delay():
    """Open browser after server starts"""
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:5000')
        print("🌐 Opened Forest Fire Emergency Interface in browser")
    except Exception as e:
        print(f"⚠️ Could not auto-open browser: {e}")
        print("   Please manually open: http://localhost:5000")

def main():
    print("🌲🔥 FOREST FIRE EMERGENCY WEB INTERFACE LAUNCHER")
    print("=" * 60)
    print("🚀 Starting web server...")
    print("📱 Interface URLs:")
    print("   Dashboard: http://localhost:5000/")
    print("   AI Chat:   http://localhost:5000/chat")
    print("   API:       http://localhost:5000/api/overview")
    print()
    print("💡 The web interface will open automatically in your browser.")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 60)
    print()
    
    # Start browser thread
    browser_thread = threading.Thread(target=open_browser_after_delay)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start the Flask application
    try:
        subprocess.run([sys.executable, "forest_fire_web_app.py"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Web server stopped")
    except Exception as e:
        print(f"\n❌ Error starting web server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
