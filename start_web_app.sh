#!/bin/bash

# Free Speech Recognition App - Streamlit Web Interface
# Startup Script

echo "🎤 Starting Free Speech Recognition Web App..."
echo "=================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup first:"
    echo "python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 1
fi

# Check if Streamlit is installed
if ! ./venv/bin/python -c "import streamlit" 2>/dev/null; then
    echo "❌ Streamlit not installed!"
    echo "Installing Streamlit..."
    ./venv/bin/pip install streamlit
fi

echo "✅ Dependencies ready!"
echo ""

# Ask user for HTTPS or HTTP
echo "🔒 Choose connection type:"
echo "1. HTTP (simple, file upload only)"
echo "2. HTTPS (required for browser recording)"
echo ""
read -p "Enter choice (1 or 2): " choice

if [ "$choice" = "2" ]; then
    # Check if SSL certificate exists
    if [ ! -f "cert.pem" ] || [ ! -f "key.pem" ]; then
        echo "🔒 Creating SSL certificate..."
        openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/C=US/ST=Local/L=Local/O=Local/OU=Local/CN=localhost"
        echo "✅ SSL certificate created!"
    fi
    
    echo "🌐 Starting HTTPS web interface..."
    echo "📍 App will be available at: https://localhost:8501"
    echo "⚠️  You'll need to accept the security warning in your browser"
    echo ""
    echo "💡 HTTPS enables:"
    echo "   • Browser microphone recording"
    echo "   • File upload (also works)"
    echo ""
    echo "🎯 Press Ctrl+C to stop the app"
    echo ""
    
    # Start with HTTPS
    ./venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0 --server.sslCertFile cert.pem --server.sslKeyFile key.pem
else
    echo "🌐 Starting HTTP web interface..."
    echo "📍 App will be available at: http://localhost:8501"
    echo ""
    echo "💡 HTTP supports:"
    echo "   • File upload transcription"
    echo "   • Manual text entry"
    echo "   • All download features"
    echo ""
    echo "ℹ️  For browser recording, restart with HTTPS (option 2)"
    echo ""
    echo "🎯 Press Ctrl+C to stop the app"
    echo ""
    
    # Start with HTTP
    ./venv/bin/streamlit run streamlit_app.py --server.port 8501 --server.address 0.0.0.0
fi
