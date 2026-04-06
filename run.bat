@echo off
REM Hospital Management System - Quick Start Script for Windows

echo.
echo ======================================================
echo  Hospital Management System - Setup Script
echo ======================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

REM Check if MySQL is installed
mysql --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: MySQL is not installed or not in PATH
    echo Please install MySQL 5.7 or higher from https://www.mysql.com/
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Installing Python dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Setting up database...
echo Please enter your MySQL root password when prompted:
mysql -u root -p < hospital_management.sql
if errorlevel 1 (
    echo ERROR: Failed to import database
    pause
    exit /b 1
)

echo.
echo [5/5] Starting the application...
echo.
echo ======================================================
echo  Hospital Management System is starting...
echo  Open your browser at http://localhost:5000
echo.
echo  Demo Credentials:
echo  - Admin: admin / password
echo  - Doctor: dr_sharma / password
echo  - Patient: patient1 / password
echo  - Receptionist: receptionist / password
echo ======================================================
echo.

python app.py

pause
