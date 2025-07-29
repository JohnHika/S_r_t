# Speech Recognition App

An advanced speech recognition application with multiple API support, pause/resume functionality, and file saving capabilities.

## Features

- **Multiple API Support**: Google Speech-to-Text, Deepgram, and CMU Sphinx
- **Language Selection**: Support for multiple languages
- **Pause/Resume**: Control recognition flow during operation
- **File Saving**: Save transcriptions to text files
- **Enhanced Error Handling**: Meaningful error messages for different scenarios

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. API Key Setup

#### Google Speech-to-Text API:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Speech-to-Text API
4. Create a Service Account and download the JSON key file
5. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
   ```

#### Deepgram API:
1. Sign up at [Deepgram Console](https://console.deepgram.com/)
2. Create an API key
3. Set environment variable:
   ```bash
   export DEEPGRAM_API_KEY="your-api-key"
   ```

#### Alternative: Use Config File
Copy `config.json.example` to `config.json` and add your credentials:
```json
{
  "api_keys": {
    "google_credentials": "/path/to/your/google-service-account.json",
    "deepgram_key": "your-deepgram-api-key"
  }
}
```

## Usage

```bash
python speech_recognition_app.py
```

### Commands During Recognition:
- `pause` - Pause speech recognition
- `resume` - Resume speech recognition
- `stop` - Stop recognition and show results
- `save` - Save current transcription to file

## Supported Languages

Common language codes:
- `en-US` - English (US)
- `en-GB` - English (UK)
- `es-ES` - Spanish (Spain)
- `fr-FR` - French
- `de-DE` - German
- `ja-JP` - Japanese
- `zh-CN` - Chinese (Simplified)

## API Comparison

| API | Accuracy | Speed | Cost | Offline |
|-----|----------|-------|------|---------|
| Google | High | Fast | Pay-per-use | No |
| Deepgram | High | Very Fast | Pay-per-use | No |
| Sphinx | Medium | Fast | Free | Yes |

## Troubleshooting

### Common Issues:

1. **Microphone not detected**: Check audio permissions and microphone connection
2. **API quota exceeded**: Check your API usage limits
3. **Network errors**: Verify internet connection for cloud APIs
4. **Audio quality issues**: Ensure quiet environment and good microphone

### Error Messages:

- "Could not understand audio" - Speak more clearly or check microphone
- "API quota exceeded" - Check your API limits or switch APIs
- "Authentication error" - Verify API credentials are correct
- "Network error" - Check internet connection

## License

MIT License
