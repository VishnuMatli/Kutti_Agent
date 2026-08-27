# J.A.R.V.I.S. Voice Assistant with Web GUI

This project integrates the Hey Kutti voice assistant with a web-based J.A.R.V.I.S.-inspired graphical user interface using Flask.

## Features

- **Voice Control**: Say "Hey Kutti" followed by commands to activate the assistant
- **Web GUI**: Futuristic J.A.R.V.I.S.-inspired interface with animated elements
- **Real-time Updates**: Dynamic data displays for time, system metrics, weather, etc.
- **Chat Interface**: Conversation history showing your commands and assistant responses
- **All Original Features**:
  - Open applications (calculator, text editor, browser, terminal)
  - Send emails with AI-assisted body rewriting
  - Set time-based reminders
  - Tell time and date
  - Answer questions using LLM (Groq/NVIDIA)
  - Cross-platform support

## Files

- `app.py`: Main Flask application that integrates with the assistant
- `assistant.py`: Core assistant logic (modified for online recognition primary)
- `templates/jarvis.html`: HTML template for the J.A.R.V.I.S. GUI
- `assistant.py.voice_backup`: Backup of original voice recognition setup
- `flask_requirements.txt`: Python dependencies for Flask

## Setup

1. Install dependencies:
   ```bash
   pip install -r flask_requirements.txt
   ```

2. Ensure your `.env` file is configured with:
   - Groq API key (or NVIDIA API key as fallback)
   - Email credentials (for email functionality)

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser to `http://localhost:5000`

## Usage

### Voice Commands
1. Click the microphone button or say "Hey Kutti" to activate listening
2. After activation, speak your command (e.g., "what time is it", "open calculator")
3. View the conversation in the chat interface
4. Hear the assistant's response through your speakers

### Available Commands
- **Applications**: "open calculator", "open text editor", "open browser", "open terminal"
- **Email**: "send email" (follow prompts)
- **Reminders**: "remind me to [task] at [HH:MM]"
- **Time/Date**: "what time is it", "what is the date"
- **General Questions**: Ask anything and get AI-powered responses
- **Exit**: "exit" or "quit" to stop the assistant

## How It Works

1. The Flask app serves the J.A.R.V.I.S. GUI at `/`
2. Voice commands are processed using the Web Speech API (browser-based)
3. Commands are sent to the backend via AJAX to `/process_command`
4. The backend uses the original `Assistant` class to process commands
5. Responses are returned and displayed in the chat interface
6. Dynamic data (time, system metrics, etc.) updates periodically

## Customization

- To change the wake word, modify the JavaScript in `templates/jarvis.html`
- To adjust assistant behavior, edit `assistant.py`
- To modify the GUI appearance, edit the CSS in `templates/jarvis.html`

## Notes

- The assistant starts in voice mode by default
- Online SpeechRecognition (Google API) is used as primary for better accuracy
- Vosk offline recognition is available as fallback in the original assistant
- For best voice recognition quality, use a good microphone in a quiet environment
- The web interface works best in modern browsers (Chrome, Firefox, Safari, Edge)

## Troubleshooting

- **Microphone not working**: Ensure your browser has permission to access the microphone
- **Speech recognition errors**: Check internet connection for online recognition
- **GUI not loading**: Make sure Flask is running and you're accessing the correct URL
- **No voice output**: Check your system's audio output and that pyttsx3 is working properly
- **Port already in use**: Change the port in `app.py` if 5000 is unavailable

## Original Assistant

The original terminal-based assistant is still available:
```bash
python assistant.py
```
It now starts in voice mode by default (online recognition primary).