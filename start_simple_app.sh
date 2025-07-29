#!/bin/bash

# Simple Speech Recognition App Launcher
# Pure Open Source - No API Keys Required

echo "🎤 Starting Simple Speech Recognition App..."
echo "Pure Open Source • No Required API Keys • Privacy-Focused"
echo

# Check if streamlit is installed
if ! command -v streamlit &> /dev/null; then
    echo "❌ Streamlit not found. Installing..."
    pip install streamlit
fi

# Check if speech_recognition is installed
python3 -c "import speech_recognition" 2>/dev/null || {
    echo "❌ SpeechRecognition not found. Installing..."
    pip install SpeechRecognition
}

# Check if pocketsphinx is installed
python3 -c "import speech_recognition as sr; sr.Recognizer().recognize_sphinx" 2>/dev/null || {
    echo "❌ PocketSphinx not found. Installing..."
    pip install pocketsphinx
}

echo "✅ All dependencies ready!"
echo
echo "🌐 Opening app in your browser..."
echo "🔧 Using CMU Sphinx (offline) by default"
echo "💡 Upload an audio file to get started"
echo
echo "Press Ctrl+C to stop the app"
echo

# Launch the streamlit app
streamlit run speech_recognition_app.py --server.port 8501 --server.headless false
