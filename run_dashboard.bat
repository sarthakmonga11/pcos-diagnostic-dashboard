@echo off
REM Quick start script for PCOS Dashboard (Windows)

echo.
echo 🏥 PCOS Diagnostic Dashboard - Quick Start
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found: 
python --version
echo.

REM Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ❌ requirements.txt not found
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo 📦 Installing dependencies...
python -m pip install -r requirements.txt -q

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully
echo.

REM Check if data exists
if not exist "data\processed\cleaned_data.csv" (
    echo ⚠️  Warning: data\processed\cleaned_data.csv not found
    echo    The dashboard will not display data until this file exists
    echo.
)

echo 🚀 Starting Streamlit dashboard...
echo    Opening at http://localhost:8501
echo.
echo Press Ctrl+C to stop the server
echo.

streamlit run app/Home.py
pause
