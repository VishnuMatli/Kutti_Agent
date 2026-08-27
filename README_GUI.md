# Hey Kutti GUI Assistant

A graphical user interface for the Hey Kutti voice assistant featuring:
- Wake word detection ("Hey Kutti")
- Animated status indicator
- Chat-style conversation display
- Voice responses using text-to-speech
- All original assistant capabilities (apps, email, reminders, etc.)

## Features

- **Modern GUI**: Dark theme with animated status circle
- **Voice Interaction**: Say "Hey Kutti" to activate, then speak your command
- **Visual Feedback**: See your commands and the assistant's responses in chat format
- **All Original Capabilities**:
  - Open applications (calculator, text editor, browser, terminal)
  - Send emails with AI-assisted body rewriting
  - Set time-based reminders
  - Tell time and date
  - Answer general questions using LLM (Groq/NVIDIA)
  - Cross-platform support

## Requirements

- All requirements from the original assistant (see requirements.txt)
- Standard Python libraries: tkinter, threading, queue
- Working microphone for voice input
- Internet connection for online speech recognition (primary) and LLM API

## Usage

1. Make sure you have configured your `.env` file with:
   - Groq API key (or NVIDIA API key as fallback)
   - Email credentials (for email functionality)

2. Run the GUI assistant:
   ```bash
   python gui_assistant.py
   ```

3. Interaction:
   - Say "Hey Kutti" to wake the assistant
   - After the wake word is detected, speak your command
   - View the conversation in the chat window
   - Hear the assistant's response via speakers

## How It Works

1. The GUI runs a background thread that continuously listens for the wake word "Hey Kutti" using online speech recognition
2. When detected, it switches to listening for a command
3. The command is processed using the original assistant's logic
4. Responses are displayed in the chat and spoken aloud
5. The status circle animates to indicate listening state

## Files

- `gui_assistant.py`: Main GUI application
- `assistant.py`: Original assistant logic (modified for online recognition primary)
- `assistant.py.voice_backup`: Backup of original voice recognition setup
- Other files unchanged from original project

## Customization

To change the wake word or adjust sensitivity, modify the `listen_for_wake_word` method in `gui_assistant.py`.

To modify the assistant's behavior or capabilities, edit `assistant.py` (the core logic remains the same).

## Troubleshooting

- **Microphone not working**: Ensure your system has a working microphone and PyAudio is properly installed
- **Speech recognition errors**: Check internet connection for online recognition; Vosk is available as fallback
- **GUI freezing**: Some commands (like web searches) may take a moment; the interface remains responsive during listening
- **No voice output**: Check your system's audio output and that pyttsx3 is working properly

## Original Assistant

The original terminal-based assistant is still available:
```bash
python assistant.py
```
It now starts in voice mode by default (online recognition primary).