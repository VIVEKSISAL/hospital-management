#!/bin/bash

# Hospital Management System - Quick Start Script for macOS/Linux

echo ""
echo "======================================================"
echo "  Hospital Management System - Setup Script"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

# Check if MySQL is installed
if ! command -v mysql &> /dev/null; then
    echo "ERROR: MySQL is not installed"
    echo "Please install MySQL 5.7 or higher from https://www.mysql.com/"
    exit 1
fi

echo "[1/5] Creating virtual environment..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to create virtual environment"
    exit 1
fi

echo "[2/5] Activating virtual environment..."
source venv/bin/activate

echo "[3/5] Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

echo ""
echo "[4/5] Setting up database..."
echo "Please enter your MySQL root password when prompted:"
mysql -u root -p < hospital_management.sql
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to import database"
    exit 1
fi

echo ""
echo "[5/5] Starting the application..."
echo ""
echo "======================================================"
echo "  Hospital Management System is starting..."
echo "  Open your browser at http://localhost:5000"
echo ""
echo "  Demo Credentials:"
echo "  - Admin: admin / password"
echo "  - Doctor: dr_sharma / password"
echo "  - Patient: patient1 / password"
echo "  - Receptionist: receptionist / password"
echo "======================================================"
echo ""

python3 app.py
