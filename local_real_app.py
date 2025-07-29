#!/usr/bin/env python3
"""
LOCAL ONLY - Real Open Source Speech Recognition
This version works locally with real transcription
"""

import streamlit as st
import speech_recognition as sr
import tempfile
import time
import os
from audio_recorder_streamlit import audio_recorder

def transcribe_real_audio(audio_file_path, language='en-US'):
    """
    REAL transcription using SpeechRecognition library
    """
    recognizer = sr.Recognizer()
    
    try:
        # Convert audio file to WAV if needed
        from pydub import AudioSegment
        
        # Load audio
        if audio_file_path.endswith('.wav'):
            with sr.AudioFile(audio_file_path) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
        else:
            # Convert to WAV first
            sound = AudioSegment.from_file(audio_file_path)
            wav_path = audio_file_path.replace(audio_file_path.split('.')[-1], 'wav')
            sound.export(wav_path, format="wav")
            
            with sr.AudioFile(wav_path) as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source)
        
        # Map language codes
        lang_map = {
            'en-US': 'en-US',
            'en-GB': 'en-GB', 
            'es-ES': 'es-ES',
            'fr-FR': 'fr-FR',
            'de-DE': 'de-DE',
            'it-IT': 'it-IT',
            'pt-PT': 'pt-PT',
            'ru-RU': 'ru-RU',
            'zh-CN': 'zh-CN'
        }
        
        target_language = lang_map.get(language, 'en-US')
        
        # Use Google's FREE speech recognition
        text = recognizer.recognize_google(audio, language=target_language)
        return text
        
    except sr.UnknownValueError:
        return "Could not understand the audio. Please try speaking more clearly."
    except sr.RequestError as e:
        return f"Error with speech recognition service: {e}"
    except Exception as e:
        return f"Error processing audio: {e}"

def main():
    """Main application"""
    st.set_page_config(
        page_title="Speech Recognition - LOCAL REAL",
        page_icon="🎤",
        layout="wide"
    )
    
    st.title("🎤 Real Open Source Speech Recognition - LOCAL")
    st.markdown("**✅ ACTUAL transcription using SpeechRecognition library**")
    
    # Status indicator
    st.success("🚀 **REAL TRANSCRIPTION** - Uses open source Google Speech Recognition!")
    st.info("🎤 **100% Open Source**: No API keys required, works offline")
    
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_language = st.selectbox(
            "🌍 Choose Language:",
            options=list(languages.keys()),
            format_func=lambda x: languages[x]
        )
    
    with col2:
        st.metric("Transcription Status", "🔊 REAL", delta="Open Source")
    
    # Recording section
    st.markdown("### 🎤 Record Audio Live")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        audio_bytes = audio_recorder(
            text="Click to record",
            recording_color="#e8b62c",
            neutral_color="#6aa36f",
            icon_name="microphone",
            icon_size="2x",
        )
    
    with col2:
        if audio_bytes:
            st.success("🎤 Audio recorded!")
            st.audio(audio_bytes, format="audio/wav")
    
    # Process recorded audio
    if audio_bytes:
        st.markdown("---")
        st.subheader("🎤 Process Recorded Audio")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info("🎵 **Source:** Live Recording")
            st.info(f"📊 **Size:** {len(audio_bytes):,} bytes")
        
        with col2:
            st.info(f"🌍 **Language:** {languages[selected_language]}")
            st.info(f"🔧 **Method:** Real SpeechRecognition")
        
        # Transcription button
        if st.button("🔄 **TRANSCRIBE RECORDING**", type="primary", use_container_width=True):
            with st.spinner("🎤 Processing your REAL audio..."):
                # Save recorded audio temporarily
                with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                    tmp_file.write(audio_bytes)
                    tmp_file_path = tmp_file.name
                
                try:
                    # Get REAL transcription
                    text = transcribe_real_audio(tmp_file_path, selected_language)
                    
                    if text and "Error" not in text and "Could not understand" not in text:
                        st.success("🎉 **REAL Transcription Complete!**")
                        
                        # Display result
                        st.markdown("### 📝 What You Actually Said:")
                        st.text_area("Your Real Speech:", value=text, height=100, disabled=True)
                        
                        # Save to history
                        timestamp = time.strftime("%H:%M:%S")
                        st.session_state.transcriptions.append({
                            'timestamp': timestamp,
                            'filename': 'Live Recording',
                            'text': text,
                            'language': languages[selected_language],
                            'method': 'Real SpeechRecognition'
                        })
                        
                        st.balloons()
                    else:
                        st.warning(f"⚠️ {text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                
                finally:
                    # Clean up
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
    
    # File upload section
    uploaded_file = st.file_uploader(
        "📁 Upload Audio File",
        type=['wav', 'mp3', 'ogg', 'flac', 'm4a'],
        help="Upload an audio file to transcribe"
    )
    
    if uploaded_file is not None:
        st.audio(uploaded_file)
        
        if st.button("🔄 **TRANSCRIBE FILE**", type="primary", use_container_width=True):
            with st.spinner("🎤 Processing uploaded file..."):
                with tempfile.NamedTemporaryFile(suffix=f".{uploaded_file.name.split('.')[-1]}", delete=False) as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name
                
                try:
                    text = transcribe_real_audio(tmp_file_path, selected_language)
                    
                    if text and "Error" not in text and "Could not understand" not in text:
                        st.success("🎉 **File Transcription Complete!**")
                        st.text_area("File Content:", value=text, height=100, disabled=True)
                        
                        timestamp = time.strftime("%H:%M:%S")
                        st.session_state.transcriptions.append({
                            'timestamp': timestamp,
                            'filename': uploaded_file.name,
                            'text': text,
                            'language': languages[selected_language],
                            'method': 'Real SpeechRecognition'
                        })
                        
                        st.balloons()
                    else:
                        st.warning(f"⚠️ {text}")
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                
                finally:
                    try:
                        os.unlink(tmp_file_path)
                    except:
                        pass
    
    # History section
    if st.session_state.transcriptions:
        st.markdown("---")
        st.header("📋 Real Transcription History")
        
        for i, trans in enumerate(reversed(st.session_state.transcriptions)):
            with st.expander(f"🎤 {trans['timestamp']} - {trans['filename']}", expanded=(i == 0)):
                st.write(f"**Language:** {trans['language']}")
                st.write(f"**Method:** {trans['method']}")
                st.write(f"**Text:** {trans['text']}")
        
        if st.button("🗑️ **Clear History**"):
            st.session_state.transcriptions = []
            st.rerun()

if __name__ == "__main__":
    main()
