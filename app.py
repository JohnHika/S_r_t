#!/usr/bin/env python3
"""
Simple Speech Recognition App - Cloud Version
Compatible with Python 3.13+ and Streamlit Cloud
"""

import streamlit as st
import tempfile
import time
import os

def check_speech_recognition():
    """Check if speech recognition is available"""
    try:
        import speech_recognition as sr
        return True, sr, None
    except ImportError as e:
        return False, None, f"SpeechRecognition library not installed: {e}"
    except Exception as e:
        return False, None, f"Error loading SpeechRecognition: {e}"

def main():
    """Main application"""
    st.set_page_config(
        page_title="Simple Speech Recognition",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎤 Simple Speech Recognition")
    st.markdown("**Upload audio files and get transcriptions using Google's free API**")
    
    # Check if speech recognition is available
    sr_available, sr_module, error_msg = check_speech_recognition()
    
    if not sr_available:
        st.error("🚨 Speech Recognition Not Available")
        st.error(f"Error: {error_msg}")
        st.info("This is likely due to Python 3.13 compatibility issues. The speech_recognition library requires Python 3.11 or earlier.")
        st.markdown("""
        ### 🔧 To fix this issue:
        1. The deployment needs Python 3.11 (check `runtime.txt`)
        2. Contact the developer to update the deployment configuration
        3. Alternative: Use a different speech recognition service
        """)
        st.stop()
    
    # Initialize session state
    if 'transcriptions' not in st.session_state:
        st.session_state.transcriptions = []
    
    # Language selection
    languages = {
        'en-US': 'English (US)',
        'en-GB': 'English (UK)',
        'es-ES': 'Spanish',
        'fr-FR': 'French',
        'de-DE': 'German',
        'it-IT': 'Italian',
        'pt-PT': 'Portuguese',
        'ru-RU': 'Russian',
        'zh-CN': 'Chinese'
    }
    
    selected_language = st.selectbox(
        "🌍 Choose Language:",
        options=list(languages.keys()),
        format_func=lambda x: languages[x]
    )
    
    # File upload
    uploaded_file = st.file_uploader(
        "📁 Upload Audio File",
        type=['wav', 'mp3', 'ogg', 'flac', 'm4a'],
        help="Upload an audio file to transcribe"
    )
    
    if uploaded_file is not None:
        st.info(f"📄 File: {uploaded_file.name} ({uploaded_file.size:,} bytes)")
        st.audio(uploaded_file)
        
        if st.button("🔄 Transcribe", type="primary"):
            try:
                # Save uploaded file temporarily
                with tempfile.NamedTemporaryFile(suffix=f".{uploaded_file.name.split('.')[-1]}", delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                # Initialize recognizer
                recognizer = sr_module.Recognizer()
                
                with st.spinner("🎤 Transcribing..."):
                    # Load audio file
                    with sr_module.AudioFile(tmp_file_path) as source:
                        recognizer.adjust_for_ambient_noise(source, duration=1)
                        audio_data = recognizer.record(source)
                    
                    # Transcribe using Google's free API
                    try:
                        text = recognizer.recognize_google(audio_data, language=selected_language)
                        
                        if text:
                            st.success("🎉 Transcription Complete!")
                            st.markdown("### 📝 Result:")
                            st.text_area("Transcribed Text:", value=text, height=100)
                            
                            # Save to history
                            timestamp = time.strftime("%H:%M:%S")
                            st.session_state.transcriptions.append({
                                'timestamp': timestamp,
                                'filename': uploaded_file.name,
                                'text': text,
                                'language': languages[selected_language]
                            })
                            
                            # Download button
                            st.download_button(
                                "💾 Download Transcription",
                                data=f"File: {uploaded_file.name}\nLanguage: {languages[selected_language]}\nTimestamp: {timestamp}\n\nText:\n{text}",
                                file_name=f"transcription_{timestamp.replace(':', '')}.txt",
                                mime="text/plain"
                            )
                            
                            st.balloons()
                        else:
                            st.warning("⚠️ No speech detected")
                    
                    except sr_module.RequestError as e:
                        st.error(f"❌ API Error: {e}")
                        st.info("💡 Google's free API has daily limits. Try again later.")
                    
                    except sr_module.UnknownValueError:
                        st.error("❌ Could not understand the audio")
                        st.info("💡 Try: Clear speech, reduce background noise, better audio quality")
                
                # Clean up
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass
                    
            except Exception as e:
                st.error(f"❌ Error: {e}")
    
    # History section
    if st.session_state.transcriptions:
        st.markdown("---")
        st.header("📋 Transcription History")
        
        for i, trans in enumerate(reversed(st.session_state.transcriptions)):
            with st.expander(f"🎤 {trans['timestamp']} - {trans['filename']}"):
                st.write(f"**Language:** {trans['language']}")
                st.write(f"**Text:** {trans['text']}")
        
        if st.button("🗑️ Clear History"):
            st.session_state.transcriptions = []
            st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "💡 **Tips:** Use clear speech, quiet environment, and supported audio formats (WAV, MP3, etc.)\n\n"
        "🔧 **Technology:** Google Speech Recognition API (Free Tier)"
    )

if __name__ == "__main__":
    main()
