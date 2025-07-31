@echo off
REM Forest Fire Emergency Response System - Quick Start Script
REM This script will start the complete system with all components

echo.
echo =====================================
echo  🔥 FOREST FIRE EMERGENCY SYSTEM 🔥
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if .env file exists
if not exist ".env" (
    echo ❌ ERROR: .env file not found
    echo Please copy .env.example to .env and configure your API key
    echo.
    echo Creating .env file from template...
    if exist ".env.example" (
        copy ".env.example" ".env"
        echo ✅ .env file created. Please edit it with your Gemini API key.
    ) else (
        echo Creating basic .env file...
        echo GEMINI_API_KEY=your_gemini_api_key_here > .env
        echo DATABASE_PATH=c:/Users/PC/OneDrive/Bureau/CERIST/web2py/applications/eden/databases/storage.db >> .env
        echo FLASK_ENV=development >> .env
        echo FLASK_DEBUG=True >> .env
        echo FLASK_HOST=127.0.0.1 >> .env
        echo FLASK_PORT=5000 >> .env
        echo ✅ Basic .env file created.
    )
    echo.
    echo Please edit .env file with your Gemini API key and restart this script.
    pause
    exit /b 1
)

echo ✅ Configuration file found
echo.

REM Install dependencies if needed
echo 📦 Checking dependencies...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo Installing Flask...
    pip install flask
)

pip show agno >nul 2>&1
if errorlevel 1 (
    echo Installing Agno framework...
    pip install agno
)

pip show google-generativeai >nul 2>&1
if errorlevel 1 (
    echo Installing Google Generative AI...
    pip install google-generativeai
)

pip show python-dotenv >nul 2>&1
if errorlevel 1 (
    echo Installing python-dotenv...
    pip install python-dotenv
)

echo ✅ All dependencies ready
echo.

REM Test system components
echo 🔍 Testing system components...

echo Testing database connection...
python -c "
try:
    from realistic_forest_fire_tool import ForestFireTool
    tool = ForestFireTool()
    print('✅ Database connection successful')
except Exception as e:
    print(f'❌ Database connection failed: {e}')
    exit(1)
" 2>nul
if errorlevel 1 (
    echo ❌ Database test failed
    echo Please check your database path in .env file
    pause
    exit /b 1
)

echo Testing AI agent...
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
if not api_key or api_key == 'your_gemini_api_key_here':
    print('❌ Please set your Gemini API key in .env file')
    exit(1)
else:
    print('✅ API key found')
" 2>nul
if errorlevel 1 (
    echo ❌ API key test failed
    echo Please set your Gemini API key in .env file
    pause
    exit /b 1
)

echo ✅ All system tests passed
echo.

REM Start the system
echo 🚀 Starting Forest Fire Emergency Response System...
echo.
echo The system will be available at:
echo 💬 Chat Interface: http://127.0.0.1:5000/chat
echo 📊 Dashboard: http://127.0.0.1:5000/
echo 🔗 API: http://127.0.0.1:5000/api/query
echo.
echo Press Ctrl+C to stop the system
echo.

REM Start the web application
python forest_fire_web_app.py

echo.
echo 🛑 Forest Fire Emergency System stopped.
pause
