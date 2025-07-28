# 🔥 Forest Fire Emergency Response AI Agent

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Agno](https://img.shields.io/badge/Agno-AI_Framework-orange.svg)](https://github.com/agno-ai/agno)
[![Gemini](https://img.shields.io/badge/Google-Gemini_1.5_Flash-yellow.svg)](https://ai.google.dev/)

## 🎯 **Overview**

A comprehensive AI-powered emergency response system designed for forest fire incidents, built with modern web technologies and advanced AI capabilities. This system provides real-time coordination, emergency management, and intelligent response planning for forest fire scenarios.

## ✨ **Key Features**

### 🤖 **AI-Powered Emergency Agent**
- **Google Gemini 1.5 Flash Integration**: Advanced natural language processing for emergency coordination
- **Real-time Fire Analysis**: Intelligent assessment of fire threats, weather conditions, and resource allocation
- **Emergency Decision Support**: AI-driven recommendations for evacuation routes, resource deployment, and tactical planning
- **Multi-language Support**: Emergency communications in multiple languages

### 🌐 **Professional Web Interface**
- **Real-time Chat Interface**: Interactive communication with the AI emergency coordinator
- **Emergency Dashboard**: Live status updates, resource tracking, and incident visualization
- **Mobile-Responsive Design**: Optimized for emergency response teams on all devices
- **Fire-Themed UI**: Professional emergency management styling with intuitive navigation

### 📊 **Database Integration**
- **Sahana Eden Integration**: Connected to comprehensive emergency management database
- **Real-time Data Access**: Live updates on resources, personnel, facilities, and incidents
- **Historical Analysis**: Access to past incident data for improved decision-making
- **Scalable Architecture**: Designed to handle multiple concurrent emergency scenarios

### 📝 **Advanced Formatting**
- **Markdown Support**: Rich text formatting for emergency reports and communications
- **Professional Reports**: Automated generation of incident reports, status updates, and resource summaries
- **Visual Indicators**: Color-coded alerts, status indicators, and priority levels
- **Emergency Emojis**: Quick visual scanning with contextual fire and emergency icons

## 🚀 **Quick Start**

### 1. **Installation**

```bash
# Clone the repository
git clone https://github.com/Karim-Merzouk/fire-incident-agent.git
cd fire-incident-agent

# Install Python dependencies
pip install -r requirements_agent.txt
pip install -r requirements_web.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your Google Gemini API key
```

### 2. **Configuration**

Create a `.env` file with your API credentials:

```env
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_PATH=/path/to/sahana/eden/database
FLASK_ENV=development
```

### 3. **Launch the System**

```bash
# Start the web interface
python forest_fire_web_app.py

# Access the system at http://localhost:5000
```

## 🏗️ **System Architecture**

### **Core Components**

#### **🤖 AI Agent (`final_forest_fire_agent.py`)**
- **Agno Framework**: Modern AI agent framework with tool integration
- **Google Gemini 1.5 Flash**: Advanced language model for emergency response
- **Tool Integration**: Database queries, weather analysis, resource planning
- **Context-Aware Responses**: Maintains emergency context across conversations

#### **🌐 Web Interface (`forest_fire_web_app.py`)**
- **Flask Backend**: Lightweight and scalable web framework
- **RESTful API**: Clean API endpoints for frontend-backend communication
- **Session Management**: Secure user sessions and emergency coordination
- **Real-time Updates**: Live status updates and emergency notifications

#### **🗄️ Database Tools (`realistic_forest_fire_tool.py`)**
- **Sahana Eden Integration**: Full access to emergency management database
- **Query Optimization**: Efficient database queries for real-time performance
- **Data Validation**: Robust error handling and data integrity checks
- **Flexible Connections**: Support for multiple database configurations

#### **🎨 Frontend (`templates/chat.html`)**
- **Modern UI/UX**: Professional emergency management interface
- **Markdown Rendering**: Rich text display for formatted emergency communications
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: WCAG compliant for emergency personnel with diverse needs

## 🔧 **Advanced Features**

### **Emergency Scenarios Supported**
- **🔥 Wildfire Response**: Comprehensive fire incident management
- **🏠 Evacuation Coordination**: Automated evacuation planning and execution
- **🚁 Resource Deployment**: Intelligent allocation of firefighting resources
- **🌡️ Weather Integration**: Real-time weather data for tactical planning
- **📡 Communication Coordination**: Multi-channel emergency communications

### **AI Capabilities**
- **Situational Awareness**: Real-time analysis of emergency conditions
- **Predictive Analysis**: AI-powered prediction of fire spread and risk assessment
- **Resource Optimization**: Intelligent allocation of personnel and equipment
- **Decision Support**: Evidence-based recommendations for emergency commanders
- **Report Generation**: Automated creation of incident reports and status updates

### **Integration Features**
- **API Endpoints**: RESTful APIs for integration with other emergency systems
- **Database Connectivity**: Seamless integration with existing emergency databases
- **External Services**: Weather APIs, mapping services, and communication platforms
- **Scalable Architecture**: Designed for deployment in large-scale emergency operations

## 📱 **Usage Examples**

### **Emergency Queries**
```
"Give me a formatted fire status report for Pine Ridge"
"Show current evacuation orders with shelter information"
"What resources are available for the Red Rock incident?"
"Create a markdown summary of today's emergency activities"
```

### **System Responses**
The AI provides professionally formatted responses with:
- **📊 Status Reports**: Detailed incident analysis and current conditions
- **🎯 Action Items**: Prioritized tasks and immediate response requirements
- **📋 Resource Lists**: Available personnel, equipment, and facilities
- **🗺️ Geographic Data**: Location-specific information and mapping coordinates

## 🛠️ **Technology Stack**

### **Backend**
- **Python 3.9+**: Modern Python with async/await support
- **Flask 2.0+**: Lightweight web framework for rapid development
- **Agno Framework**: Advanced AI agent framework with tool integration
- **SQLite/PostgreSQL**: Flexible database support for various deployment scenarios

### **AI & ML**
- **Google Gemini 1.5 Flash**: State-of-the-art language model for emergency response
- **Natural Language Processing**: Advanced text understanding and generation
- **Context Management**: Sophisticated conversation and emergency context handling
- **Tool Integration**: Seamless AI-database interaction for real-time data access

### **Frontend**
- **HTML5/CSS3**: Modern web standards with emergency-optimized styling
- **JavaScript ES6+**: Interactive features and real-time updates
- **Markdown Parsing**: Client-side rendering of formatted emergency communications
- **Responsive Design**: Bootstrap-inspired responsive grid system

### **Database**
- **Sahana Eden**: Comprehensive emergency management database schema
- **Real-time Queries**: Optimized database access for emergency response times
- **Data Integrity**: Robust validation and error handling for critical data
- **Scalable Design**: Architecture supports large-scale emergency operations

## 🚨 **Emergency Deployment**

### **Production Setup**
```bash
# Production environment setup
export FLASK_ENV=production
export GEMINI_API_KEY=your_production_api_key

# Launch with production settings
python forest_fire_web_app.py --host=0.0.0.0 --port=5000
```

### **Security Considerations**
- **API Key Protection**: Secure storage and rotation of API credentials
- **Database Security**: Encrypted connections and access control
- **User Authentication**: Secure login for emergency personnel
- **Data Privacy**: Compliance with emergency data protection regulations

## 📚 **Documentation**

### **Implementation Guides**
- `FOREST_FIRE_SYSTEM_COMPLETE.md`: Complete system implementation details
- `WEB_INTERFACE_COMPLETE.md`: Web interface setup and customization
- `GEMINI_INTEGRATION_COMPLETE.md`: AI integration and configuration
- `MARKDOWN_IMPLEMENTATION_COMPLETE.md`: Rich text formatting implementation

### **API Documentation**
- **Chat Endpoint**: `POST /api/query` - Send emergency queries to AI agent
- **Status Endpoint**: `GET /api/status` - System health and status information
- **Database Endpoint**: `GET /api/data` - Access emergency database information

## 🤝 **Contributing**

We welcome contributions to improve the Forest Fire Emergency Response System:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/emergency-enhancement`
3. **Make your changes** and test thoroughly
4. **Commit with clear messages**: `git commit -m "Add weather integration feature"`
5. **Push to your fork**: `git push origin feature/emergency-enhancement`
6. **Create a Pull Request** with detailed description

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 **Emergency Support**

For immediate technical support during emergency operations:
- **GitHub Issues**: [Report bugs or request features](https://github.com/Karim-Merzouk/fire-incident-agent/issues)
- **Emergency Contact**: Create urgent issues with `[EMERGENCY]` tag for priority response

## 🏆 **Acknowledgments**

- **Sahana Software Foundation**: For the comprehensive emergency management framework
- **Google AI**: For the powerful Gemini language model
- **Agno Framework**: For the modern AI agent development platform
- **Emergency Response Community**: For requirements and feedback that shaped this system

---

## 🔥 **Ready for Emergency Response!**

This Forest Fire Emergency Response AI Agent represents the cutting edge of emergency management technology, combining advanced AI capabilities with practical emergency response needs. The system is designed by emergency management professionals for real-world deployment in forest fire scenarios.

**🌲 Deploy. Coordinate. Save Lives. 🔥**

---

*Built with ❤️ for emergency responders and forest protection teams worldwide.*
