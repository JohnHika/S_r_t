#!/usr/bin/env python3
"""
Simple Speech Recognition App - Pure Open Source
No API keys required - uses offline CMU Sphinx
"""

import streamlit as st
import speech_recognition as sr
import tempfile
import time
import os
from pathlib import Path

class SimpleSpeechApp:
    """Clean, simple speech recognition using only open-source tools"""
    
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
        """Get list of available open-source speech recognition APIs"""
        return {
            'sphinx': 'CMU Sphinx (Offline)',
            'google_free': 'Google (Free Tier)',
            'whisper': 'OpenAI Whisper (Local) - Coming Soon'
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
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
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
        """Save transcription to a text file"""
        if not filename:
            filename = f"transcription_{time.strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            # Create downloads directory if it doesn't exist
            downloads_dir = Path.home() / "Downloads"
            downloads_dir.mkdir(exist_ok=True)
            
            file_path = downloads_dir / filename
            
            # Write transcription with metadata
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(f"Speech Recognition Transcription\n")
                f.write(f"Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Language: {self.get_supported_languages()[st.session_state.selected_language]}\n")
                f.write(f"API: {self.get_available_apis()[st.session_state.recognition_api]}\n")
                f.write(f"{'='*50}\n\n")
                f.write(text)
            
            return str(file_path)
        except Exception as e:
            st.error(f"Error saving file: {str(e)}")
            return None
    
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
                "🎯 **Pure Open Source**\n\n"
                "• CMU Sphinx: 100% offline\n"
                "• Google Free: Limited daily usage\n"
                "• No paid API keys required\n"
                "• Privacy-focused"
            )
    
    def record_5_seconds(self):
        """Record exactly 5 seconds of audio using PyAudio"""
        try:
            import pyaudio
            
            # Audio recording parameters
            CHUNK = 1024
            FORMAT = pyaudio.paInt16
            CHANNELS = 1
            RATE = 16000
            RECORD_SECONDS = 5
            
            # Initialize PyAudio
            p = pyaudio.PyAudio()
            
            # Open stream
            stream = p.open(format=FORMAT,
                          channels=CHANNELS,
                          rate=RATE,
                          input=True,
                          frames_per_buffer=CHUNK)
            
            st.info("🎤 **Recording for 5 seconds...** Speak now!")
            
            frames = []
            
            # Create a progress bar for the 5-second recording
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
                
                # Update progress
                progress = (i + 1) / (RATE / CHUNK * RECORD_SECONDS)
                progress_bar.progress(progress)
                remaining = RECORD_SECONDS - (i * CHUNK / RATE)
                status_text.text(f"🔴 Recording... {remaining:.1f} seconds remaining")
            
            # Stop recording
            stream.stop_stream()
            stream.close()
            p.terminate()
            
            progress_bar.progress(1.0)
            status_text.text("✅ Recording complete!")
            
            # Save to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp_file:
                import wave
                wf = wave.open(tmp_file.name, 'wb')
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(p.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(b''.join(frames))
                wf.close()
                
                return tmp_file.name
                
        except ImportError:
            st.error("❌ PyAudio not installed. Install with: pip install pyaudio")
            return None
        except Exception as e:
            st.error(f"❌ Recording error: {str(e)}")
            return None
    
    def display_quick_record_section(self):
        """Display 5-second quick recording section"""
        st.header("🎤 Quick 5-Second Recording")
        
        # Show current status
        if st.session_state.is_paused:
            st.warning("⏸️ **Transcription is currently PAUSED.** Use the Resume button in the sidebar to continue.")
            return
        
        st.markdown("**Just click the button below and speak for 5 seconds. That's it!**")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"🌍 **Language:** {self.get_supported_languages()[st.session_state.selected_language]}")
            st.info(f"🔧 **API:** {self.get_available_apis()[st.session_state.recognition_api]}")
        
        with col2:
            st.markdown("💡 **Tips:**")
            st.markdown("• Speak clearly")
            st.markdown("• Stay close to mic")
            st.markdown("• Minimize background noise")
        
        # Big record button
        if st.button("🔴 **RECORD 5 SECONDS**", type="primary", use_container_width=True):
            # Record audio
            audio_file_path = self.record_5_seconds()
            
            if audio_file_path:
                with st.spinner("🎤 Transcribing your 5-second recording..."):
                    try:
                        # Load the recorded audio
                        with sr.AudioFile(audio_file_path) as source:
                            self.recognizer.adjust_for_ambient_noise(source, duration=1)
                            audio_data = self.recognizer.record(source)
                        
                        # Transcribe based on selected API
                        text = None
                        error = None
                        
                        if st.session_state.recognition_api == 'sphinx':
                            try:
                                text = self.recognizer.recognize_sphinx(
                                    audio_data, 
                                    language=st.session_state.selected_language
                                )
                            except sr.RequestError:
                                try:
                                    text = self.recognizer.recognize_sphinx(audio_data)
                                except sr.RequestError as e:
                                    error = f"Sphinx recognition service error: {str(e)}"
                                except sr.UnknownValueError:
                                    error = "Could not understand the speech. Try speaking more clearly."
                            except sr.UnknownValueError:
                                error = "Could not understand the speech. Try speaking more clearly."
                        
                        elif st.session_state.recognition_api == 'google_free':
                            try:
                                text = self.recognizer.recognize_google(
                                    audio_data,
                                    language=f"{st.session_state.selected_language}-{st.session_state.selected_language.upper()}"
                                )
                            except sr.RequestError as e:
                                if "quota" in str(e).lower() or "limit" in str(e).lower():
                                    error = "Google API quota exceeded. Try using CMU Sphinx instead."
                                else:
                                    error = f"Google recognition service error: {str(e)}"
                            except sr.UnknownValueError:
                                error = "Google could not understand the speech."
                        
                        # Clean up temp file
                        try:
                            os.unlink(audio_file_path)
                        except:
                            pass
                        
                        # Display result
                        if error:
                            st.error(f"❌ **Error:** {error}")
                            if "understand" in error.lower():
                                st.info("💡 **Try:** Speaking louder, clearer, or closer to the microphone")
                        elif text and str(text).strip():
                            # Success!
                            st.success("🎉 **5-Second Recording Transcribed!**")
                            
                            # Display result in a nice box
                            st.markdown("### 📝 What You Said:")
                            st.markdown(f"**\"{text}\"**")
                            
                            # Save to history
                            timestamp = time.strftime("%H:%M:%S")
                            st.session_state.transcriptions.append({
                                'timestamp': timestamp,
                                'filename': '5-second recording',
                                'text': str(text),
                                'language': st.session_state.selected_language,
                                'api': st.session_state.recognition_api
                            })
                            
                            # Success animation
                            st.balloons()
                            
                            # Auto-save option
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.button("💾 Save This", use_container_width=True):
                                    saved_path = self.save_transcription_to_file(str(text), f"5sec_recording_{timestamp.replace(':', '')}.txt")
                                    if saved_path:
                                        st.success(f"✅ Saved to: {saved_path}")
                            
                            with col2:
                                if st.button("🔄 Record Again", use_container_width=True):
                                    st.rerun()
                        else:
                            st.warning("⚠️ **No speech detected** in the 5-second recording. Try speaking louder.")
                            
                    except Exception as e:
                        st.error(f"❌ **Unexpected error:** {str(e)}")
                        try:
                            os.unlink(audio_file_path)
                        except:
                            pass
    
    def display_file_upload_section(self):
        """Display file upload interface"""
        st.header("📁 Upload Audio File")
        
        # Show current status
        if st.session_state.is_paused:
            st.warning("⏸️ **Transcription is currently PAUSED.** Use the Resume button in the sidebar to continue.")
            return
        
        uploaded_file = st.file_uploader(
            "Choose an audio file to transcribe",
            type=['wav', 'mp3', 'ogg', 'flac', 'm4a', 'aac'],
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
        """Display transcription history with save options"""
        if st.session_state.transcriptions:
            st.header("📋 Transcription History")
            
            # Bulk operations
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("💾 Save All to File"):
                    transcription_parts = [
                        f"[{trans['timestamp']}] {trans['filename']}\n{trans['text']}"
                        for trans in st.session_state.transcriptions
                    ]
                    all_text = "\n\n" + "="*50 + "\n\n".join(transcription_parts)
                    saved_path = self.save_transcription_to_file(all_text, "all_transcriptions.txt")
                    if saved_path:
                        st.success(f"✅ Saved to: {saved_path}")
            
            with col2:
                # Download button for all transcriptions
                if st.session_state.transcriptions:
                    transcription_lines = [
                        f"[{trans['timestamp']}] {trans['filename']}\nLanguage: {trans['language']}\nAPI: {trans['api']}\n{trans['text']}"
                        for trans in st.session_state.transcriptions
                    ]
                    all_text = "\n\n".join(transcription_lines)
                    st.download_button(
                        "📥 Download All",
                        data=all_text,
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
                        # Individual save button
                        if st.button(f"💾 Save", key=f"save_{i}"):
                            filename = f"transcription_{trans['timestamp'].replace(':', '')}.txt"
                            saved_path = self.save_transcription_to_file(trans['text'], filename)
                            if saved_path:
                                st.success(f"Saved!")
        else:
            st.info("🔇 **No transcriptions yet.** Upload an audio file to get started!")
    
    def run(self):
        """Main application runner"""
        # Page configuration
        st.set_page_config(
            page_title="Simple Speech Recognition",
            page_icon="🎤",
            layout="wide",
            initial_sidebar_state="expanded"
        )
        
        # Main header
        st.title("🎤 Simple Speech Recognition App")
        st.markdown("**Pure Open Source • No Required API Keys • Privacy-Focused**")
        
        # Settings sidebar
        self.display_settings_sidebar()
        
        # Main content tabs
        tab1, tab2, tab3 = st.tabs(["🎤 Quick Record (5s)", "📁 Upload & Transcribe", "📋 History"])
        
        with tab1:
            self.display_quick_record_section()
        
        with tab2:
            self.display_file_upload_section()
        
        with tab3:
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
                "• Keep recordings under 5 minutes"
            )
        
        with col2:
            st.markdown(
                "🆘 **Troubleshooting:**\n"
                "• If Google API fails, use CMU Sphinx\n"
                "• For poor quality, try different language\n"
                "• Use Pause/Resume to control processing\n"
                "• Check Downloads folder for saved files"
            )

# Run the application
if __name__ == "__main__":
    app = SimpleSpeechApp()
    app.run()
