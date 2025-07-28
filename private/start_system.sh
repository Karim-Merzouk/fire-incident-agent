#!/bin/bash

# Forest Fire Emergency Response System - Quick Start Script
# This script will start the complete system with all components

echo ""
echo "====================================="
echo " 🔥 FOREST FIRE EMERGENCY SYSTEM 🔥"
echo "====================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ ERROR: Python 3 is not installed${NC}"
    echo "Please install Python 3.9+ from https://python.org"
    exit 1
fi

echo -e "${GREEN}✅ Python found${NC}"
echo ""

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ ERROR: .env file not found${NC}"
    echo "Please copy .env.example to .env and configure your API key"
    echo ""
    echo "Creating .env file from template..."
    
    if [ -f ".env.example" ]; then
        cp ".env.example" ".env"
        echo -e "${GREEN}✅ .env file created. Please edit it with your Gemini API key.${NC}"
    else
        echo "Creating basic .env file..."
        cat > .env << EOL
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_PATH=/absolute/path/to/your/sahana/eden/database/storage.db
FLASK_ENV=development
FLASK_DEBUG=True
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
EOL
        echo -e "${GREEN}✅ Basic .env file created.${NC}"
    fi
    
    echo ""
    echo "Please edit .env file with your Gemini API key and restart this script."
    exit 1
fi

echo -e "${GREEN}✅ Configuration file found${NC}"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Install dependencies if needed
echo -e "${YELLOW}📦 Checking dependencies...${NC}"

pip show flask &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing Flask..."
    pip install flask
fi

pip show agno &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing Agno framework..."
    pip install agno
fi

pip show google-generativeai &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing Google Generative AI..."
    pip install google-generativeai
fi

pip show python-dotenv &> /dev/null
if [ $? -ne 0 ]; then
    echo "Installing python-dotenv..."
    pip install python-dotenv
fi

echo -e "${GREEN}✅ All dependencies ready${NC}"
echo ""

# Test system components
echo -e "${BLUE}🔍 Testing system components...${NC}"

echo "Testing database connection..."
python3 -c "
try:
    from realistic_forest_fire_tool import ForestFireTool
    tool = ForestFireTool()
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Database test failed${NC}"
    echo "Please check your database path in .env file"
    exit 1
fi

echo "Testing AI agent..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key or api_key == 'your_gemini_api_key_here':
    print('❌ Please set your Gemini API key in .env file')
    exit(1)
else:
    print('✅ API key found')
" 2>/dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ API key test failed${NC}"
    echo "Please set your Gemini API key in .env file"
    exit 1
fi

echo -e "${GREEN}✅ All system tests passed${NC}"
echo ""

# Start the system
echo -e "${BLUE}🚀 Starting Forest Fire Emergency Response System...${NC}"
echo ""
echo "The system will be available at:"
echo "💬 Chat Interface: http://127.0.0.1:5000/chat"
echo "📊 Dashboard: http://127.0.0.1:5000/"
echo "🔗 API: http://127.0.0.1:5000/api/query"
echo ""
echo "Press Ctrl+C to stop the system"
echo ""

# Start the web application
python3 forest_fire_web_app.py

echo ""
echo -e "${YELLOW}🛑 Forest Fire Emergency System stopped.${NC}"
