# 🎤 Free Speech Recognition Web App

A **completely free** web-based speech recognition application that works without any API keys! Perfect for users who can't access Google Speech API (requires payment) or Deepgram.

## ✨ Features

### 🆓 **Completely Free**
- **No API keys required** - No Google, Deepgram, or other paid services
- **No internet required** for transcription - Works completely offline
- **No usage limits** - Process as many files as you want

### 🌐 **Web Interface**
- **Streamlit-powered** - Beautiful, responsive web interface
- **File upload support** - Upload WAV, MP3, OGG, FLAC, M4A files
- **Real-time feedback** - See transcription results immediately
- **Multi-language support** - 8+ languages supported

### 💾 **Export & Save**
- **Download transcriptions** as text files
- **Timestamped exports** - Keep track of when each transcription was made
- **Session history** - View all transcriptions in current session

## 🚀 Quick Start

### 1. Run the App
```bash
cd /home/john-hika/Public/S_R_A
./venv/bin/streamlit run streamlit_app.py
```

### 2. Open in Browser
- The app will automatically open at `http://localhost:8501`
- Or manually visit the URL shown in the terminal

### 3. Upload & Transcribe
1. **Upload an audio file** (WAV recommended)
2. **Click "Transcribe Audio"**
3. **View results** and download transcriptions

## 🎯 Supported Audio Formats

| Format | Compatibility | Recommended |
|--------|---------------|-------------|
| **WAV** | ✅ Excellent | ⭐ **Best** |
| **FLAC** | ✅ Excellent | ⭐ Great |
| **MP3** | ⚠️ Good | ✓ OK |
| **OGG** | ⚠️ Good | ✓ OK |
| **M4A** | ⚠️ Variable | ✓ OK |

## 🌍 Supported Languages

- 🇺🇸 **English (US)** - `en-US`
- 🇬🇧 **English (UK)** - `en-GB`
- 🇪🇸 **Spanish** - `es-ES`
- 🇫🇷 **French** - `fr-FR`
- 🇩🇪 **German** - `de-DE`
- 🇮🇹 **Italian** - `it-IT`
- 🇵🇹 **Portuguese** - `pt-PT`
- 🇷🇺 **Russian** - `ru-RU`

## 💡 Tips for Best Results

### 📁 **File Preparation**
- Use **WAV format** for best compatibility
- Keep files **under 1 minute** for faster processing
- Ensure **clear audio quality**

### 🎤 **Recording Tips**
- Speak **clearly and slowly**
- Minimize **background noise**
- Use a **good microphone** if possible
- Maintain **consistent volume**

### 🔧 **Troubleshooting**
- **No speech detected?** → Try a different file format or speak more clearly
- **Poor accuracy?** → Use WAV format and ensure clear audio
- **App won't start?** → Check that all dependencies are installed

## 🏗️ Technical Details

### **Speech Recognition Engine**
- **CMU Sphinx (PocketSphinx)** - Mature, offline speech recognition
- **No cloud dependency** - Everything runs locally
- **Privacy-focused** - Audio never leaves your computer

### **Web Framework**
- **Streamlit** - Modern Python web framework
- **Responsive design** - Works on desktop and mobile
- **Real-time updates** - Interactive user experience

## 🆚 Comparison with Other Solutions

| Feature | This App | Google Speech | Deepgram |
|---------|----------|---------------|----------|
| **Cost** | 🆓 Free | 💰 Paid | 💰 Paid |
| **Internet** | ❌ Not required | ✅ Required | ✅ Required |
| **API Keys** | ❌ None needed | ✅ Required | ✅ Required |
| **Privacy** | 🔒 Complete | ⚠️ Cloud-based | ⚠️ Cloud-based |
| **Accuracy** | ⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Excellent | ⭐⭐⭐⭐⭐ Excellent |
| **Speed** | ⭐⭐⭐⭐ Fast | ⭐⭐⭐⭐⭐ Very Fast | ⭐⭐⭐⭐⭐ Very Fast |

## 📱 Using the Web Interface

### **Main Features**
1. **Upload Area** - Drag & drop or click to upload audio files
2. **Language Selector** - Choose your language in the sidebar
3. **Transcription History** - View all processed files
4. **Download Options** - Export results as text files
5. **Manual Text Entry** - Add text manually if needed

### **Session Management**
- **Auto-save** - All transcriptions saved during session
- **Clear function** - Reset all data with one click
- **Export options** - Multiple download formats available

## 🎊 Perfect for:

- **Students** who need free transcription tools
- **Content creators** on a budget
- **Privacy-conscious users** who want offline processing
- **Developers** who need API-free solutions
- **Anyone** who can't access paid APIs

---

**🎤 Start transcribing for free - no accounts, no keys, no limits!**
