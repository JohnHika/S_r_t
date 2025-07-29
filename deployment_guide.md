# 🚀 Streamlit Cloud Deployment Guide

## 📋 Step-by-Step Deployment Instructions

### 1. 📁 Repository Structure for Deployment

Your repository is now set up with these key files:

```
S_R_A/
├── app.py                    # ← MAIN FILE for Streamlit Cloud
├── speech_recognition_app.py # Local version with microphone
├── requirements.txt          # Dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── README.md                # Documentation
└── deployment_guide.md      # This guide
```

### 2. 🌐 Deploy to Streamlit Cloud

#### Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit - Speech Recognition App"
git branch -M main
git push -u origin main
```

#### Step 2: Create Deployment Branch
```bash
git checkout -b deployment
git push -u origin deployment
```

#### Step 3: Go to Streamlit Cloud
1. Visit: https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account
4. Select repository: `JohnHika/S_r_t`
5. **Choose branch: `deployment`**
6. **Main file path: `app.py`** ← Important!

### 3. ⚙️ Streamlit Cloud Configuration

#### Repository Settings:
- **Repository**: `https://github.com/JohnHika/S_r_t.git`
- **Branch**: `deployment`
- **Main file**: `app.py`
- **Python version**: 3.8+ (automatic)

#### Advanced Settings (Optional):
```
[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

### 4. 📦 Dependencies (requirements.txt)
Your requirements.txt is optimized for cloud deployment:
```
streamlit==1.47.1
SpeechRecognition==3.10.0
pocketsphinx==5.0.0
numpy
pathlib
```

### 5. 🔄 Two Versions Explanation

#### Cloud Version (`app.py`) - For Streamlit Cloud
- ✅ **File upload transcription**
- ✅ **CMU Sphinx (offline)**
- ✅ **Google Speech API (free tier)**
- ❌ **No microphone recording** (cloud limitation)
- ✅ **Download transcriptions**
- ✅ **Multi-language support**

#### Local Version (`speech_recognition_app.py`) - For Local Use
- ✅ **File upload transcription**
- ✅ **5-second microphone recording**
- ✅ **CMU Sphinx (offline)**
- ✅ **Google Speech API (free tier)**
- ✅ **All features included**

### 6. 🎯 Deployment Commands

#### Push Main Branch:
```bash
git add .
git commit -m "Production ready - Cloud deployment"
git push origin main
```

#### Push Deployment Branch:
```bash
git checkout deployment
git merge main
git push origin deployment
```

### 7. 📱 Expected Cloud URL
After deployment, your app will be available at:
```
https://your-app-name.streamlit.app/
```

### 8. 🔧 Local Testing Before Deployment

Test the cloud version locally:
```bash
streamlit run app.py
```

Test the full local version:
```bash
streamlit run speech_recognition_app.py
```

### 9. 🚨 Important Notes

#### For Streamlit Cloud:
- **Use `app.py` as main file** (not `speech_recognition_app.py`)
- **PyAudio removed** from requirements (not needed for cloud)
- **Microphone recording disabled** (browser security in cloud)
- **File upload works perfectly**
- **All transcription features work**

#### Cloud Limitations:
- No microphone access (browser security)
- File upload only
- CMU Sphinx works offline
- Google API has daily limits

### 10. ✅ Deployment Checklist

- [ ] Repository pushed to GitHub
- [ ] `app.py` is the main file
- [ ] `requirements.txt` has correct dependencies
- [ ] `.streamlit/config.toml` configured
- [ ] `deployment` branch created
- [ ] Streamlit Cloud app configured
- [ ] App URL tested and working

### 11. 🎉 Post-Deployment

After successful deployment:
1. **Test file upload** with various audio formats
2. **Try different languages**
3. **Test download functionality**
4. **Share your app URL**

### 12. 🔄 Future Updates

To update your deployed app:
```bash
git add .
git commit -m "Update: [describe changes]"
git push origin main
git checkout deployment
git merge main
git push origin deployment
```

The Streamlit Cloud app will automatically redeploy!

---

## 🎯 Summary

**Main file for deployment**: `app.py`
**Branch to deploy**: `deployment`
**Repository**: `https://github.com/JohnHika/S_r_t.git`

Your app will be a fully functional speech recognition service accessible worldwide! 🌍
