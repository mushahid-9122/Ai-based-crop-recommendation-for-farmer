@echo off
REM Crop Recommendation System - Windows Setup Script
REM This script automates the setup process for both backend and frontend

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo   Crop Recommendation System - Setup Script (Windows)
echo ========================================================
echo.

REM Check prerequisites
echo Checking prerequisites...

python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo OK: Python is installed

node --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Node.js is not installed or not in PATH
    pause
    exit /b 1
)
echo OK: Node.js is installed

npm --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: npm is not installed or not in PATH
    pause
    exit /b 1
)
echo OK: npm is installed

REM Setup Backend
echo.
echo Setting up Backend...

cd backend

echo Creating Python virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Failed to install Python dependencies
    pause
    exit /b 1
)

echo OK: Backend setup complete

cd ..

REM Setup Frontend
echo.
echo Setting up Frontend...

cd frontend

echo Installing Node.js dependencies...
call npm install

if errorlevel 1 (
    echo ERROR: Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo OK: Frontend setup complete

cd ..

REM Summary
echo.
echo ========================================================
echo Setup Complete!
echo ========================================================
echo.
echo Next Steps:
echo.
echo 1. Train the ML models:
echo    cd backend
echo    venv\Scripts\activate
echo    jupyter notebook crop_recommendation_model.ipynb
echo.
echo 2. Start backend API (new terminal):
echo    cd backend
echo    venv\Scripts\activate
echo    python app.py
echo.
echo 3. Start frontend (another new terminal):
echo    cd frontend
echo    npm start
echo.
echo 4. Open browser: http://localhost:3000
echo.
echo For more information, see QUICKSTART.md
echo.
pause
