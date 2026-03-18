#!/bin/bash
# Quick start script for PCOS Dashboard

echo "🏥 PCOS Diagnostic Dashboard - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python found: $(python3 --version)"
echo ""

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found. Please run this script from the project root directory."
    exit 1
fi

echo "📦 Installing dependencies..."
pip install -r requirements.txt --quiet

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed successfully"
echo ""

# Check if data exists
if [ ! -f "data/processed/cleaned_data.csv" ]; then
    echo "⚠️  Warning: data/processed/cleaned_data.csv not found"
    echo "   The dashboard will not display data until this file exists."
    echo ""
fi

echo "🚀 Starting Streamlit dashboard..."
echo "   Opening at http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app/Home.py
