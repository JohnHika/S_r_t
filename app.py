#!/usr/bin/env python3
"""
Speech Recognition App - Cloud Deployment Version
Optimized for Streamlit Cloud without system audio dependencies
"""

import streamlit as st
import speech_recognition as sr
import tempfile
import time
import os
from pathlib import Path

class CloudSpeechApp:
    """Cloud-optimized Speech Recognition App"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.setup_session_state()
    
    def setup_session_state(self):
        """Initialize session state variables"""
        if 'transcriptions' not in st.session_state:
            st.session_state.transcriptions = []
        if 'selected_language' not in st.session_state:
            st.session_state.selected_language = 'en'
        if 'recognition_api' not in st.session_state:
            st.session_state.recognition_api = 'sphinx'
        if 'is_paused' not in st.session_state:
            st.session_state.is_paused = False
    
    def get_available_apis(self):
        """Get list of available speech recognition APIs for cloud"""
        return {
            'sphinx': 'CMU Sphinx (Offline)',
            'google_free': 'Google (Free Tier)'
        }
    
    def get_supported_languages(self):
        """Get supported languages for speech recognition"""
        return {
            'en': 'English',
            'es': 'Spanish', 
            'fr': 'French',
            'de': 'German',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'zh': 'Chinese'
        }
    
    def transcribe_audio_file(self, audio_file):
        """Transcribe uploaded audio file with improved error handling"""
        try:
            # Check if paused
            if st.session_state.is_paused:
                return None, "Transcription is paused. Click 'Resume' to continue."
            
            # Save uploaded file temporarily
            with tempfile.NamedTemporaryFile(suffix=f".{audio_file.name.split('.')[-1]}", delete=False) as tmp_file:
                tmp_file.write(audio_file.getvalue())
                tmp_file_path = tmp_file.name
            
            # Load and process audio
            with sr.AudioFile(tmp_file_path) as source:
                # Adjust for ambient noise to improve accuracy
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio_data = self.recognizer.record(source)
            
            # Perform transcription based on selected API
            if st.session_state.recognition_api == 'sphinx':
                try:
                    # Try with selected language first
                    text = self.recognizer.recognize_sphinx(
                        audio_data, 
                        language=st.session_state.selected_language
                    )
                except sr.RequestError:
                    # Fallback to English if language not supported
                    try:
                        text = self.recognizer.recognize_sphinx(audio_data)
                    except sr.RequestError as e:
                        return None, f"Sphinx recognition service error: {str(e)}"
                    except sr.UnknownValueError:
                        return None, "Could not understand the speech in the audio file. Try speaking more clearly or reducing background noise."
            
            elif st.session_state.recognition_api == 'google_free':
                try:
                    # Use Google's free tier (has daily limits)
                    text = self.recognizer.recognize_google(
                        audio_data,
                        language=f"{st.session_state.selected_language}-{st.session_state.selected_language.upper()}"
                    )
                except sr.RequestError as e:
                    if "quota" in str(e).lower() or "limit" in str(e).lower():
                        return None, "Google API quota exceeded. Try using CMU Sphinx instead."
                    return None, f"Google recognition service error: {str(e)}"
                except sr.UnknownValueError:
                    return None, "Google could not understand the speech in the audio file."
            
            else:
                return None, f"API '{st.session_state.recognition_api}' not yet implemented"
            
            # Clean up temporary file
            try:
                os.unlink(tmp_file_path)
            except:
                pass
            
            return text.strip() if text else None, None
            
        except sr.RequestError as e:
            return None, f"Speech recognition service error: {str(e)}"
        except Exception as e:
            return None, f"Unexpected error during transcription: {str(e)}"
    
    def save_transcription_to_file(self, text, filename=None):
        """Save transcription to a downloadable format"""
        if not filename:
            filename = f"transcription_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Create content with metadata
        content = f"Speech Recognition Transcription\n"
        content += f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        content += f"Language: {self.get_supported_languages()[st.session_state.selected_language]}\n"
        content += f"API: {self.get_available_apis()[st.session_state.recognition_api]}\n"
        content += f"{'='*50}\n\n"
        content += text
        
        return content
    
    def display_settings_sidebar(self):
        """Display settings in sidebar"""
        with st.sidebar:
            st.header("⚙️ Settings")
            
            # API Selection
            st.subheader("🔧 Recognition API")
            apis = self.get_available_apis()
            st.session_state.recognition_api = st.selectbox(
                "Choose API:",
                options=list(apis.keys()),
                format_func=lambda x: apis[x],
                index=0,
                help="CMU Sphinx works offline, Google Free has daily limits"
            )
            
            # Language Selection
            st.subheader("🌍 Language")
            languages = self.get_supported_languages()
            st.session_state.selected_language = st.selectbox(
                "Choose language:",
                options=list(languages.keys()),
                format_func=lambda x: languages[x],
                index=0
            )
            
            # Pause/Resume Control
            st.subheader("⏯️ Control")
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("⏸️ Pause", disabled=st.session_state.is_paused):
                    st.session_state.is_paused = True
                    st.rerun()
            
            with col2:
                if st.button("▶️ Resume", disabled=not st.session_state.is_paused):
                    st.session_state.is_paused = False
                    st.rerun()
            
            # Status indicator
            if st.session_state.is_paused:
                st.warning("⏸️ Transcription PAUSED")
            else:
                st.success("▶️ Transcription ACTIVE")
            
            # Info section
            st.info(
                "🎯 **Cloud Deployment**\n\n"
                "• CMU Sphinx: 100% offline\n"
                "• Google Free: Limited daily usage\n"
                "• No microphone access in cloud\n"
                "• Upload audio files to transcribe\n"
                "• Privacy-focused"
            )
    
    def display_file_upload_section(self):
        """Display file upload interface"""
        st.header("📁 Upload Audio File")
        
        # Show current status
        if st.session_state.is_paused:
            st.warning("⏸️ **Transcription is currently PAUSED.** Use the Resume button in the sidebar to continue.")
            return
        
        # Cloud deployment notice
        st.info("☁️ **Cloud Version**: Upload your audio files to transcribe. Microphone recording is not available in cloud deployment.")
        
        uploaded_file = st.file_uploader(
            "Choose an audio file to transcribe",
            type=['wav', 'mp3', 'ogg', 'flac', 'm4a', 'aac', 'webm'],
            help="Upload any audio file containing speech"
        )
        
        if uploaded_file is not None:
            # Display file information
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"📄 **File:** {uploaded_file.name}")
                st.info(f"📊 **Size:** {uploaded_file.size:,} bytes")
            
            with col2:
                st.info(f"🌍 **Language:** {self.get_supported_languages()[st.session_state.selected_language]}")
                st.info(f"🔧 **API:** {self.get_available_apis()[st.session_state.recognition_api]}")
            
            # Audio player
            st.audio(uploaded_file, format=uploaded_file.type)
            
            # Transcription controls
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("🔄 **TRANSCRIBE**", type="primary", use_container_width=True):
                    with st.spinner("🎤 Transcribing your audio..."):
                        text, error = self.transcribe_audio_file(uploaded_file)
                        
                        if error:
                            st.error(f"❌ **Error:** {error}")
                            if "understand" in error.lower():
                                st.info("💡 **Try:** Speaking more clearly, reducing background noise, or using a different audio format")
                            elif "quota" in error.lower() or "limit" in error.lower():
                                st.info("💡 **Try:** Using CMU Sphinx (offline) instead of Google API")
                        elif text:
                            # Success!
                            st.success("🎉 **Transcription Complete!**")
                            
                            # Display result
                            st.markdown("### 📝 Transcribed Text:")
                            st.text_area("", value=text, height=100, disabled=True)
                            
                            # Save to history
                            timestamp = time.strftime("%H:%M:%S")
                            st.session_state.transcriptions.append({
                                'timestamp': timestamp,
                                'filename': uploaded_file.name,
                                'text': text,
                                'language': st.session_state.selected_language,
                                'api': st.session_state.recognition_api
                            })
                            
                            st.balloons()
                            st.rerun()
                        else:
                            st.warning("⚠️ **No speech detected** in the audio file")
            
            with col2:
                # Clear/Reset button
                if st.button("🗑️ **CLEAR**", use_container_width=True):
                    st.rerun()
    
    def display_transcription_history(self):
        """Display transcription history with download options"""
        if st.session_state.transcriptions:
            st.header("📋 Transcription History")
            
            # Bulk operations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Download All"):
                    transcription_parts = [
                        f"[{trans['timestamp']}] {trans['filename']}\n{trans['text']}"
                        for trans in st.session_state.transcriptions
                    ]
                    all_text = "\n\n" + "="*50 + "\n\n".join(transcription_parts)
                    content = self.save_transcription_to_file(all_text, "all_transcriptions.txt")
                    
                    st.download_button(
                        "📥 Download File",
                        data=content,
                        file_name=f"transcriptions_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            with col2:
                # Download button for all transcriptions
                if st.session_state.transcriptions:
                    transcription_lines = [
                        f"[{trans['timestamp']}] {trans['filename']}\nLanguage: {trans['language']}\nAPI: {trans['api']}\n{trans['text']}"
                        for trans in st.session_state.transcriptions
                    ]
                    all_text = "\n\n".join(transcription_lines)
                    content = self.save_transcription_to_file(all_text)
                    
                    st.download_button(
                        "📥 Quick Download",
                        data=content,
                        file_name=f"transcriptions_{time.strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain"
                    )
            
            with col3:
                if st.button("🗑️ Clear History"):
                    st.session_state.transcriptions = []
                    st.success("History cleared!")
                    st.rerun()
            
            # Display individual transcriptions
            st.markdown("---")
            for i, trans in enumerate(reversed(st.session_state.transcriptions)):
                with st.expander(
                    f"🎤 {trans['timestamp']} - {trans['filename']} ({trans['language']})",
                    expanded=(i == 0)
                ):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.write(f"**Text:** {trans['text']}")
                        st.caption(f"Language: {self.get_supported_languages()[trans['language']]} | API: {self.get_available_apis()[trans['api']]}")
                    
                    with col2:
                        # Individual download button
                        content = self.save_transcription_to_file(trans['text'], f"transcription_{trans['timestamp'].replace(':', '')}.txt")
                        st.download_button(
                            f"💾 Download",
                            data=content,
                            file_name=f"transcription_{trans['timestamp'].replace(':', '')}.txt",
                            mime="text/plain",
                            key=f"download_{i}"
                        )
        else:
            st.info("🔇 **No transcriptions yet.** Upload an audio file to get started!")
    
    def run(self):
        """Main application runner"""
        # Page configuration
        st.set_page_config(
            page_title="Speech Recognition - Cloud",
            page_icon="🎤",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Main header
        st.title("🎤 Speech Recognition App - Cloud Edition")
        st.markdown("**Pure Open Source • No Required API Keys • Cloud Optimized**")
        
        # Settings sidebar
        self.display_settings_sidebar()
        
        # Main content tabs
        tab1, tab2 = st.tabs(["📁 Upload & Transcribe", "📋 History"])
        
        with tab1:
            self.display_file_upload_section()
        
        with tab2:
            self.display_transcription_history()
        
        # Footer with instructions
        st.markdown("---")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                "💡 **Tips for Best Results:**\n"
                "• Record in a quiet environment\n"
                "• Speak clearly and at normal pace\n"
                "• Use WAV format when possible\n"
                "• Keep recordings under 10 minutes"
            )
        
        with col2:
            st.markdown(
                "☁️ **Cloud Deployment Notes:**\n"
                "• File upload only (no microphone)\n"
                "• CMU Sphinx runs offline\n"
                "• Google API has daily limits\n"
                "• Download transcriptions locally"
            )

# Run the application
if __name__ == "__main__":
    app = CloudSpeechApp()
    app.run()
