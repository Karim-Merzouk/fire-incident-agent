# 🔥 Forest Fire Emergency Response System - Complete Setup & Execution Guide

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Agno](https://img.shields.io/badge/Agno-AI_Framework-orange.svg)](https://github.com/agno-ai/agno)
[![Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Flash-yellow.svg)](https://ai.google.dev/)

## 📋 **Table of Contents**

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Execution](#execution)
5. [Usage](#usage)
6. [Troubleshooting](#troubleshooting)
7. [System Architecture](#system-architecture)

---

## 🔧 **Prerequisites**

### **System Requirements**
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python**: 3.9 or higher
- **Memory**: Minimum 4GB RAM (8GB recommended)
- **Storage**: 2GB free space
- **Internet Connection**: Required for Gemini API access

### **Required Accounts**
- **Google AI Studio Account**: For Gemini API key
  - Visit: https://ai.google.dev/
  - Create account and generate API key

---

## 🚀 **Installation**

### **Step 1: Clone or Download the Project**

**Option A: If you have Git:**
```bash
git clone https://github.com/Karim-Merzouk/fire-incident-agent.git
cd fire-incident-agent
```

**Option B: Manual Download:**
1. Download all files from the project repository
2. Extract to your desired directory
3. Navigate to the project folder

### **Step 2: Set Up Python Environment**

**Create Virtual Environment (Recommended):**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### **Step 3: Install Dependencies**

**Install all required packages:**
```bash
# Install AI Agent dependencies
pip install -r requirements_agent.txt

# Install Web Interface dependencies
pip install -r requirements_web.txt

# Or install everything at once
pip install -r requirements_complete.txt
```

**Manual Installation (if requirements files are missing):**
```bash
pip install agno flask google-generativeai python-dotenv requests sqlite3
```

---

## ⚙️ **Configuration**

### **Step 1: Environment Variables**

**Create `.env` file in the project root:**
```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_gemini_api_key_here

# Database Configuration
DATABASE_PATH=c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000

# Logging
LOG_LEVEL=INFO
```

### **Step 2: Get Your Gemini API Key**

1. **Visit Google AI Studio**: https://ai.google.dev/
2. **Sign in** with your Google account
3. **Create a new project** or select existing one
4. **Generate API Key**:
   - Go to "Get API Key" section
   - Click "Create API Key"
   - Copy the generated key
5. **Add to `.env` file**:
   ```env
   GEMINI_API_KEY=AIzaSyD65ZjWvlddTalQB2lwOCUgVScBb_oN_pI
   ```

### **Step 3: Database Configuration**

**Update database path in `.env`:**
```env
# Update this path to match your system
DATABASE_PATH=/absolute/path/to/your/sahana/eden/database/storage.db
```

**For Windows:**
```env
DATABASE_PATH=C:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db
```

**For macOS/Linux:**
```env
DATABASE_PATH=/home/username/path/to/eden/databases/storage.db
```

---

## 🎯 **Execution**

### **Method 1: Quick Start (Recommended)**

**Launch the complete system:**
```bash
# Activate virtual environment (if using)
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Start the Forest Fire Emergency Response System
python forest_fire_web_app.py
```

**Expected Output:**
```
🔥 Starting Forest Fire Emergency Response System...
✅ Environment variables loaded
✅ Gemini API initialized
✅ Database connection established
✅ AI Agent configured
🌐 Web server starting...
 * Running on http://127.0.0.1:5000
 * Debug mode: True
🚀 Forest Fire Emergency Response System is READY!
```

### **Method 2: Component Testing**

**Test Individual Components:**

**1. Test AI Agent:**
```bash
python final_forest_fire_agent.py
```

**2. Test Database Connection:**
```bash
python test_db_connection.py
```

**3. Test Complete System:**
```bash
python test_complete_system.py
```

### **Method 3: Development Mode**

**For developers wanting to modify the system:**
```bash
# Set development environment
export FLASK_ENV=development
export FLASK_DEBUG=True

# Start with auto-reload
python forest_fire_web_app.py
```

---

## 📱 **Usage**

### **Access the System**

Once the system is running, access it through your web browser:

**Main URLs:**
- **Chat Interface**: http://localhost:5000/chat
- **Dashboard**: http://localhost:5000/
- **API Endpoint**: http://localhost:5000/api/query

### **Using the Chat Interface**

**Example Emergency Queries:**
```
1. "Give me a formatted fire status report for Pine Ridge National Forest"
2. "Show current evacuation orders with shelter information"
3. "What firefighting resources are available in the Red Rock area?"
4. "Create a markdown summary of today's emergency activities"
5. "Analyze weather conditions for fire spread prediction"
```

### **Expected Response Format**

The AI will provide professionally formatted responses with:

**✅ Rich Markdown Formatting:**
- ## Headers for main topics
- ### Subheaders for categories
- **Bold text** for critical information
- *Italic text* for emphasis
- • Bullet points for lists
- 🔥🚨🏠 Emergency emojis for visual context

**✅ Emergency Information:**
- Fire size and containment status
- Evacuation zones and shelter locations
- Resource deployment and availability
- Weather conditions and forecasts
- Communication coordinates

---

## 🔍 **Troubleshooting**

### **Common Issues & Solutions**

#### **1. Import Errors**
```
Error: ModuleNotFoundError: No module named 'agno'
```
**Solution:**
```bash
pip install agno
# Or try:
pip install git+https://github.com/agno-ai/agno.git
```

#### **2. Database Connection Issues**
```
Error: Database not available
```
**Solution:**
1. Check database path in `.env` file
2. Ensure Sahana Eden database exists
3. Verify file permissions
```bash
# Test database connection
python test_db_connection.py
```

#### **3. Gemini API Errors**
```
Error: API key not valid
```
**Solution:**
1. Verify API key in `.env` file
2. Check Google AI Studio quota
3. Ensure internet connection
```bash
# Test API connection
python -c "import os; from google.generativeai import configure; configure(api_key=os.getenv('GEMINI_API_KEY')); print('✅ API key valid')"
```

#### **4. Port Already in Use**
```
Error: Address already in use
```
**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID_NUMBER> /F

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Or use different port
python forest_fire_web_app.py --port 5001
```

#### **5. Template Not Found**
```
Error: Template 'chat.html' not found
```
**Solution:**
```bash
# Ensure templates directory exists
mkdir -p templates
# Copy template files from the project
```

### **Debugging Commands**

**Check System Status:**
```bash
# Test all components
python test_complete_system.py

# Check markdown formatting
python test_markdown_formatting.py

# Validate database structure
python check_table_structure.py
```

**View Logs:**
```bash
# Check Flask logs
tail -f flask.log

# Check system logs
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

---

## 🏗️ **System Architecture**

### **Core Components**

#### **1. Web Interface (`forest_fire_web_app.py`)**
- **Framework**: Flask web server
- **Port**: 5000 (default)
- **Features**: Chat interface, API endpoints, static file serving
- **Templates**: HTML templates with emergency styling

#### **2. AI Agent (`final_forest_fire_agent.py`)**
- **Framework**: Agno AI framework
- **Model**: Google Gemini 1.5 Flash
- **Features**: Emergency analysis, markdown formatting, tool integration

#### **3. Database Tool (`realistic_forest_fire_tool.py`)**
- **Database**: Sahana Eden SQLite
- **Features**: Real-time data access, emergency records, resource tracking

#### **4. Frontend (`templates/chat.html`)**
- **Technologies**: HTML5, CSS3, JavaScript
- **Features**: Markdown rendering, responsive design, emergency theming

### **File Structure**
```
fire-incident-agent/
├── 📄 forest_fire_web_app.py          # Main web server
├── 🤖 final_forest_fire_agent.py      # AI agent
├── 🗄️ realistic_forest_fire_tool.py   # Database tool
├── 📋 requirements_*.txt               # Dependencies
├── ⚙️ .env                            # Configuration
├── 📁 templates/
│   └── 💬 chat.html                   # Chat interface
├── 📁 static/
│   ├── 🎨 styles.css                  # Emergency styling
│   └── ⚡ scripts.js                   # Interactive features
└── 📚 docs/                           # Documentation
    ├── 📖 COMPLETE_SETUP_GUIDE.md     # This guide
    ├── 🔧 SYSTEM_COMPLETE.md          # Technical details
    └── 📝 MARKDOWN_IMPLEMENTATION.md  # Formatting guide
```

### **Data Flow**

1. **User Input** → Chat Interface (`chat.html`)
2. **HTTP Request** → Flask Server (`forest_fire_web_app.py`)
3. **Query Processing** → AI Agent (`final_forest_fire_agent.py`)
4. **Database Query** → Database Tool (`realistic_forest_fire_tool.py`)
5. **AI Response** → Gemini 1.5 Flash Model
6. **Markdown Formatting** → Response Processing
7. **JSON Response** → Chat Interface
8. **HTML Rendering** → User Display

---

## 🎯 **Advanced Usage**

### **API Integration**

**Direct API Calls:**
```bash
# POST request to query endpoint
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Forest fire status report"}'
```

**Python API Usage:**
```python
import requests

response = requests.post(
    'http://localhost:5000/api/query',
    json={'query': 'Emergency status update'}
)
print(response.json()['response'])
```

### **Custom Deployment**

**Production Deployment:**
```bash
# Set production environment
export FLASK_ENV=production
export FLASK_HOST=0.0.0.0
export FLASK_PORT=80

# Run with Gunicorn (recommended)
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 forest_fire_web_app:app
```

**Docker Deployment:**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements_complete.txt
EXPOSE 5000
CMD ["python", "forest_fire_web_app.py"]
```

---

## 📞 **Support & Contributions**

### **Getting Help**
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Read additional guides in `/docs`
- **Community**: Join discussions about emergency response systems

### **Contributing**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/emergency-enhancement`)
3. Commit changes (`git commit -m "Add weather integration"`)
4. Push to branch (`git push origin feature/emergency-enhancement`)
5. Create Pull Request

---

## 🏆 **Success Indicators**

**✅ System Successfully Running When:**
- Web server starts without errors
- Chat interface loads at http://localhost:5000/chat
- AI responses are formatted with markdown
- Database queries return emergency data
- No error messages in console/logs

**✅ Ready for Emergency Operations When:**
- All status checks pass
- API responses are under 3 seconds
- Markdown formatting displays correctly
- Database connections are stable
- All emergency features are functional

---

## 🚨 **Emergency Deployment Checklist**

**Pre-Deployment:**
- [ ] All dependencies installed
- [ ] API keys configured and tested
- [ ] Database connection verified
- [ ] System tests passed
- [ ] Network connectivity confirmed

**Deployment:**
- [ ] Start web server
- [ ] Verify chat interface loads
- [ ] Test emergency queries
- [ ] Confirm markdown formatting
- [ ] Validate response times

**Post-Deployment:**
- [ ] Monitor system logs
- [ ] Test all emergency scenarios
- [ ] Verify real-time data access
- [ ] Confirm scalability for multiple users
- [ ] Document any issues or observations

---

## 🌟 **System Ready for Emergency Response!**

This Forest Fire Emergency Response System is now configured and ready to provide professional emergency coordination and response support. The AI agent provides intelligent analysis, the web interface offers intuitive interaction, and the integrated database ensures access to critical emergency information.

**🔥 Deploy. Coordinate. Save Lives. 🌲**

---

*Built with ❤️ for emergency responders and forest protection teams worldwide.*

**Last Updated**: July 28, 2025
**Version**: 2.0.0
**Status**: Production Ready 🟢
