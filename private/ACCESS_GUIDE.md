# 🔥 HOW TO ACCESS YOUR FOREST FIRE AI AGENT

## 🎯 **Multiple Ways to Access Your AI Agent:**

### **Method 1: Direct URL Access (Recommended)**
1. Open your browser
2. Go to: `http://127.0.0.1:8000/eden/fire/ai_agent`
3. Start chatting with your AI agent!

### **Method 2: From Disease Tracking Page**
1. Go to Disease Tracking module (currently visible in menu)
2. Look for the **red alert box** with "Forest Fire Emergency AI Agent"
3. Click **"Launch Fire Emergency AI Agent"** button

### **Method 3: From Main Dashboard**
1. Go to the main Eden homepage: `http://127.0.0.1:8000/eden`
2. Look for the **fire-themed panel** with gradient background
3. Click **"Launch AI Agent"** button

### **Method 4: Enable Fire Module in Menu**
To make the Fire module appear in the main menu bar:

1. **Restart the Web2py Server:**
   ```powershell
   # Stop current server (Ctrl+C)
   # Then restart:
   cd c:\Users\PC\OneDrive\Bureau\CERIST\web2py
   python web2py.py -a password -i 127.0.0.1 -p 8000
   ```

2. **Check Menu Bar:** After restart, you should see "Fire Stations" in the menu

3. **Access AI Agent:** Fire Stations → AI Emergency Agent

---

## 🚀 **Quick Test Steps:**

### **Test 1: Direct Access**
- URL: `http://127.0.0.1:8000/eden/fire/ai_agent`
- Expected: Chat interface with red/orange fire theme

### **Test 2: Fire Module Homepage**
- URL: `http://127.0.0.1:8000/eden/fire`
- Expected: Fire station page with "Launch AI Assistant" button

### **Test 3: AI Agent Functionality**
- Send message: "What fire emergency assistance can you provide?"
- Expected: AI responds with forest fire emergency capabilities

---

## 🔧 **Troubleshooting:**

### **If AI Agent Page Doesn't Load:**
- Check URL is exactly: `http://127.0.0.1:8000/eden/fire/ai_agent`
- Ensure Web2py server is running
- Check browser console for JavaScript errors

### **If Menu Doesn't Show Fire Module:**
- Restart Web2py server completely
- Clear browser cache
- Check that 000_config.py was modified correctly

### **If AI Doesn't Respond:**
- Check .env file has GEMINI_API_KEY configured
- Verify internet connection for AI API access
- Check terminal for Python error messages

---

## 📋 **Configuration Files Modified:**

### **Enabled Fire Module:**
- `models/000_config.py` - Added fire module configuration
- `models/fire_menu.py` - Menu integration (optional)

### **Added Quick Access:**
- `views/default/index.html` - Main dashboard access
- `views/disease/index.html` - Disease tracking page access
- `views/fire/index.html` - Fire module homepage

### **Core AI Integration:**
- `controllers/fire.py` - AI agent controller functions
- `views/fire/ai_agent.html` - Chat interface
- `private/final_forest_fire_agent.py` - AI agent core
- `private/realistic_forest_fire_tool.py` - Database tool

---

## 🎉 **Success Indicators:**

✅ **Fire Module Enabled**: Should appear in menu after restart  
✅ **AI Agent Accessible**: Direct URL loads chat interface  
✅ **Quick Access Added**: Buttons visible on main pages  
✅ **Database Connected**: AI can query emergency data  
✅ **Professional UI**: Fire-themed emergency styling  

---

## 📞 **Immediate Access:**

**🔥 DIRECT AI AGENT LINK:** 
http://127.0.0.1:8000/eden/fire/ai_agent

**🏠 FIRE MODULE HOMEPAGE:**
http://127.0.0.1:8000/eden/fire

**Your Forest Fire Emergency AI Agent is ready!** 🌲🔥🤖
