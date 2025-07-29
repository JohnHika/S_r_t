# 🔬 Recording Debug Guide

## Testing Browser Recording Step-by-Step

### ✅ **What to Watch For:**

1. **When you click START:**
   - Status should change to "🔴 Recording..."
   - Frame counter should start appearing and increasing
   - Debug info should show "Captured frames: X" (where X increases)

2. **While recording:**
   - Speak clearly into your microphone
   - Watch the frame count increase in real-time
   - You should see "📊 Frames captured: X" where X keeps growing

3. **When you click STOP:**
   - Status should change back to "⭕ Ready to record"
   - Frame count should remain visible
   - You should see the total number of captured frames

4. **When you click Process Recording:**
   - Should show processing messages like:
     - "Processing X audio frames..."
     - "Combined audio shape: (Y,)"
     - "Created WAV file: /tmp/..."
     - "Audio loaded for recognition..."
     - "Sphinx result: 'your text'"

### 🔧 **Debugging Steps:**

#### **Step 1: Check Frame Capture**
- Click START and speak
- **Expected:** Frame counter increases while you speak
- **If not working:** Microphone permission issue

#### **Step 2: Check Audio Length**
- Record for at least 3-5 seconds
- **Expected:** Frame count should be 100+ frames
- **If too few:** Record longer or speak louder

#### **Step 3: Check Processing**
- Click Process Recording
- **Expected:** See debug messages about processing
- **If errors:** Check the specific error message

### 🎯 **Common Issues & Solutions:**

#### **"No audio recorded" but frame count is 0:**
```
Problem: Audio frames not being captured
Solutions:
1. Refresh the page
2. Allow microphone access again
3. Check browser console for errors (F12)
4. Try a different browser (Chrome works best)
```

#### **Frame count increases but "No audio recorded":**
```
Problem: Audio frames captured but empty
Solutions:
1. Speak louder/closer to microphone
2. Check microphone isn't muted
3. Test microphone in other apps first
```

#### **Frames captured but processing fails:**
```
Problem: Audio processing/transcription issue
Solutions:
1. Record for longer (5+ seconds)
2. Speak more clearly
3. Reduce background noise
4. Try the file upload method instead
```

### 🎤 **Quick Test Protocol:**

1. **Visit:** `https://localhost:8501`
2. **Go to:** "🎙️ Record Audio" tab
3. **Click:** START
4. **Say:** "Hello this is a test recording" (slowly and clearly)
5. **Watch:** Frame counter should increase
6. **Click:** STOP
7. **Check:** Frame count should be 50+ frames
8. **Click:** Process Recording
9. **Expect:** Transcription of your speech

### 📱 **Alternative Test (Always Works):**

If browser recording still doesn't work:

1. **Record on your phone** (voice memo app)
2. **Transfer file to computer** (email/cloud/USB)
3. **Go to "📁 Upload File" tab**
4. **Upload the audio file**
5. **Click "Transcribe Uploaded File"**

This method bypasses all browser/HTTPS issues!

### 🆘 **Emergency Fallback:**

If nothing works, create a simple test file:

```bash
# Create a test audio file
# Record using built-in recorder:
# - Windows: Sound Recorder
# - Mac: QuickTime Player
# - Linux: GNOME Sound Recorder

# Or use command line (if available):
arecord -f cd -t wav -d 5 test.wav
# Then upload test.wav via the file upload tab
```

---

**Remember: The app works either way - browser recording OR file upload! 🎉**
