# 🔧 Troubleshooting Browser Recording

## Common Issues and Solutions

### ❌ **Error: "navigator.mediaDevices is undefined"**

**Problem:** Browser recording requires HTTPS (secure connection)

**Solutions:**

#### **Option 1: Use HTTPS (Recommended)**
```bash
# Stop current app
pkill -f streamlit

# Start with HTTPS
./start_web_app.sh
# Choose option 2 when prompted

# Visit: https://localhost:8501
# Accept certificate warning when prompted
```

#### **Option 2: Chrome with Insecure Localhost**
```bash
# Start Chrome with special flag
google-chrome --unsafely-treat-insecure-origin-as-secure=http://localhost:8501 --user-data-dir=/tmp/chrome_dev_test
```

#### **Option 3: Use File Upload Instead**
- Record audio with your phone or computer
- Save as WAV file
- Upload via "📁 Upload File" tab
- Works without HTTPS!

---

### ❌ **Certificate Warning in Browser**

**Problem:** "Your connection is not private" warning

**Solution:**
1. Click **"Advanced"**
2. Click **"Proceed to localhost (unsafe)"**
3. This is safe for localhost development

---

### ❌ **Microphone Access Denied**

**Problem:** Browser won't access microphone

**Solutions:**
1. **Check browser permissions:**
   - Look for microphone icon in address bar
   - Click and select "Allow"

2. **Reset site permissions:**
   - Chrome: Settings → Privacy → Site Settings → Microphone
   - Firefox: Address bar → Shield icon → Permissions

3. **System microphone settings:**
   - Ensure microphone is not muted
   - Check default microphone device

---

### ❌ **No Audio Recorded**

**Problem:** Recording doesn't capture audio

**Solutions:**
1. **Check microphone connection**
2. **Test in other apps first**
3. **Try different browser**
4. **Refresh the page**
5. **Clear browser cache**

---

### ❌ **Poor Transcription Quality**

**Problem:** Inaccurate transcription results

**Solutions:**
1. **Improve audio quality:**
   - Speak closer to microphone
   - Reduce background noise
   - Use external microphone if possible

2. **Recording technique:**
   - Speak clearly and slowly
   - Record 2-10 seconds at a time
   - Pause between words/sentences

3. **Try file upload instead:**
   - Record with dedicated audio app
   - Save as high-quality WAV
   - Upload for better results

---

## 🚀 Quick Fix Commands

### **Restart with HTTPS:**
```bash
pkill -f streamlit
./start_web_app.sh
# Choose option 2
```

### **Restart with HTTP (file upload only):**
```bash
pkill -f streamlit
./start_web_app.sh
# Choose option 1
```

### **Reset browser permissions:**
```bash
# Chrome
google-chrome --reset-permissions --user-data-dir=/tmp/chrome_dev_test

# Or just use incognito/private browsing
```

---

## 🔍 Browser Compatibility

| Browser | HTTP Support | HTTPS Support | Recommendation |
|---------|-------------|---------------|----------------|
| **Chrome** | File upload only | ✅ Full support | ⭐ **Best** |
| **Firefox** | File upload only | ✅ Full support | ⭐ **Great** |
| **Safari** | File upload only | ⚠️ May need config | ✓ OK |
| **Edge** | File upload only | ✅ Full support | ⭐ **Great** |

---

## 💡 Alternative Workflows

### **If Browser Recording Won't Work:**

1. **Mobile Phone Recording:**
   - Use voice memo app
   - Export as audio file
   - Upload via file tab

2. **Computer Recording:**
   - Use built-in voice recorder
   - Or apps like Audacity
   - Save as WAV format

3. **Online Recording Tools:**
   - Record in browser elsewhere
   - Download the file
   - Upload to this app

---

## 🆘 Still Having Issues?

### **Try This Step-by-Step:**

1. **Close all browser tabs**
2. **Run:** `./start_web_app.sh`
3. **Choose:** Option 2 (HTTPS)
4. **Visit:** `https://localhost:8501`
5. **Accept** certificate warning
6. **Allow** microphone access
7. **Test** recording

### **If All Else Fails:**
- Use the **"📁 Upload File"** tab
- This always works regardless of HTTPS/HTTP
- Record audio elsewhere and upload

---

**Remember: The app is completely free either way! 🎉**
