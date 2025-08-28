#!/bin/bash

# Wild Pick 2.0 - Brand Guidelines Color Palette Explorer
# Run script for the enhanced color palette application

echo "🎨 Starting Wild Pick 2.0 - Brand Guidelines Color Palette Explorer..."
echo "✨ Features:"
echo "   • Large circular color swatches in neat grid"
echo "   • Complete color information (CMYK, RGB, HEX)"
echo "   • Tint strips (75% and 50%) for each color"
echo "   • Harmony Playground with Complementary, Analogous, and Triadic colors"
echo "   • Export functionality for JSON harmonies"
echo "   • Clean, minimal brand guidelines style"
echo ""

# Check if virtual environment exists and activate it
if [ -d "venv" ]; then
    echo "📦 Activating virtual environment..."
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Using system Python."
fi

# Check for required packages
echo "🔍 Checking dependencies..."
python -c "import streamlit, numpy, PIL, sklearn, colorsys" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✅ All required packages are installed"
else
    echo "❌ Missing required packages. Installing..."
    pip install streamlit numpy pillow scikit-learn
fi

# Run the application
echo "🚀 Launching Wild Pick 2.0..."
echo "📱 The app will open in your default browser"
echo "🔗 If it doesn't open automatically, go to: http://localhost:8502"
echo ""

streamlit run wild_pick_2.py --server.port 8502

echo "👋 Thanks for using Wild Pick 2.0!"

