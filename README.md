# JARVIS‑Like Multimodal Assistant (Hey Kutti)

A modular, cross‑platform personal assistant that responds to the wake word **“Hey Kutti”**, uses a large language model (Groq/NVIDIA) for understanding, can launch applications, send emails, tell time/date, and is ready to be extended with hand/face gestures, eye‑tracking, and a futuristic holographic GUI.

---

## Features

| Feature | Status | Description |
|---------|--------|-------------|
| **Wake‑word detection** | ✅ (text mode) | Listens for “Hey Kutti” and replies with a personalized greeting. |
| **LLM integration** | ✅ (Groq API) | Sends user queries to a large language model (default `groq/compound`) and speaks the answer. |
| **Command handling** | ✅ | Recognizes keywords: `calculator`, `open browser`, `open text editor`, `open terminal`, `send email`, `time`, `date`, `exit`. |
| **Email sending** | ✅ | Uses Gmail SMTP with App Password; can read credentials from `.env` or prompt interactively. |
| **Cross‑platform app launch** | ✅ | Works on Windows, macOS, and Linux (opens default apps). |
| **Extensible design** | 🛠️ | Voice, gesture, face, eye‑tracking, and GUI modules can be plugged in. |
| **Text‑based operation** | ✅ | Fully functional without audio dependencies (useful for development). |

---

## Project Structure

```
/home/vishnu/Desktop/kutti
│
├─ assistant.py          # Main assistant logic
├─ .env                  # API keys & email credentials (see Configuration)
├─ requirements.txt      # Python dependencies
├─ README.md             # This file
├─ SUCCESS_SUMMARY.md   # Detailed feasibility & next‑steps guide
└─ (optional) demo.py    # Simple demonstration script
```

---

## Installation & Setup

### 1. Clone / Create the project folder
```bash
mkdir -p ~/Desktop/kutti
cd ~/Desktop/kutti
```

### 2. Create a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install Python dependencies
```bash
pip install -r requirements.txt
```

`requirements.txt` currently contains:
```
SpeechRecognition==3.10.0
pyttsx3==2.90
python-dotenv==1.0.1
requests==2.32.3
openai==1.50.0   # used only if you switch to the NVIDIA endpoint
```

> **Note:** The `SpeechRecognition` package requires the system library `portaudio`.  
> On Debian/Ubuntu install it with:
> ```bash
> sudo apt-get install portaudio19-dev
> ```
> Then reinstall `pyaudio`:
> ```bash
> pip install --force-reinstall pyaudio
> ```

### 4. Configure environment variables
Copy the example below into a file named `.env` in the project root (no quotes around values).

```dotenv
# ---- LLM Provider (Groq recommended) ----
GROQ_API_KEY=your_groq_api_key_here
GROQ_API_BASE=https://api.groq.com/openai/v1
GROQ_LLM_MODEL=groq/compound   # check https://console.groq.com/docs/models for current options

# ---- Optional NVIDIA fallback (if you prefer) ----
# NVIDIA_API_KEY=your_nvidia_api_key_here
# NVIDIA_API_BASE=https://integrate.api.nvidia.com/v1
# NVIDIA_LLM_MODEL=nvidia/nemotron-3-super-120b-a12b

# ---- Email credentials (Gmail) ----
EMAIL_USER=your_email@gmail.com
EMAIL_APP_PASSWORD=your_gmail_app_password   # generate via Google Account → Security → App Passwords
# Optional defaults for non‑interactive sending
EMAIL_TO=recipient@example.com
EMAIL_SUBJECT=Test from Assistant
EMAIL_BODY=This is a test email sent by the assistant.
```

> **Important:** Do **not** wrap values in quotes. The `.env` parser reads raw strings.

### 5. Run the assistant (text mode)
```bash
python assistant.py
```

You should see:
```
Assistant: Assistant initialized. Waiting for wake word 'Hey Kutti'...
```

Now type a line that includes the wake word, e.g.:
```
hey kutti what is the capital of france?
```

The assistant will:
1. Detect the wake word,
2. Greet you,
3. Send the remainder of the line to the LLM,
4. Speak (print) the answer.

Try commands like:
- `calculator` → opens the system calculator
- `open browser` → opens your default web browser
- `open text editor` → opens gedit/kate/notepad
- `send email` → sends an email using the values in `.env` (or prompts if you run the script in a terminal)
- `exit` → quits the program

---

## How to Enable Voice Input/Output

The assistant is built to support speech, but the current environment is missing the `aifc` module (part of Python’s standard library), causing `speech_recognition` to fail. To enable voice:

1. **Fix the Python standard library**  
   - On Debian/Ubuntu:  
     ```bash
     sudo apt-get install python3-stdlib-extensions
     ```
   - Or recreate the virtual environment with a complete Python interpreter:
     ```bash
     deactivate
     rm -rf venv
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

2. **Install the audio dependency** (if not already present):
   ```bash
   pip install pyaudio   # requires portaudio19-dev (see above)
   ```

3. Switch to voice mode by editing `assistant.py`:
   ```python
   assistant = Assistant(use_voice=True)   # instead of False
   ```

4. Run the assistant again and speak:  
   ```
   Hey Kutti, what is the weather today?
   ```

   You should hear the assistant’s response via the default audio output.

---

## Extending the Assistant

### Gesture & Face Control
- Install MediaPipe and OpenCV:
  ```bash
  pip install opencv-python mediapipe
  ```
- Use `mediapipe.solutions.hands` and `mediapipe.solutions.face_mesh` to detect landmarks.
- Map gestures (swipe, pinch, eye‑blink) to commands by calling the existing methods (`open_calculator`, `send_email`, etc.).

### Eye‑Tracking Cursor
- Libraries like `webgazer` (via a simple HTML/JS overlay) or custom pupil‑tracking with OpenCV can move the mouse pointer.
- Integrate with `pyautogui` to perform clicks based on dwell time.

### Futuristic Holographic GUI
- Use **Three.js** or **Babylon.js** to create a 3D scene with floating panels.
- Render the scene in a full‑screen, transparent window (Electron, CEF, or a custom OpenGL context).
- Accept input from gaze/gesture/voice to interact with holographic widgets.

### Agentic Task Planning
- Enhance the LLM prompt with a “chain‑of‑thought” or “ReAct” style:
  ```
  You are an assistant that can use tools: open_app, send_email, get_time, etc.
  User: "Email John about the meeting tomorrow at 3 pm."
  Thought: I need to find John’s contact, draft the email, then send it.
  Action: lookup_contact("John")
  ...
  ```
- Implement simple tool functions that the LLM can call via a JSON‑based protocol.

---

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `ModuleNotFoundError: No module named 'aifc'` | Incomplete Python stdlib (common in some custom builds) | Reinstall Python or install `python3-stdlib-extensions`; recreate venv. |
| `pyaudio` installation fails | Missing `portaudio` development headers | `sudo apt-get install portaudio19-dev` then `pip install --force-reinstall pyaudio`. |
| Email sending fails with `Username and Password not accepted` | Wrong credentials or 2‑Step Verification not enabled | Ensure 2‑Step Verification is on; use an **App Password**, not your regular password; double‑check `.env` values (no quotes). |
| LLM returns 400/413 errors | Invalid model name or request too large | Verify the model exists in the provider’s list (Groq: `groq/compound`, `openai/gpt-oss-20b`, etc.); reduce `max_tokens` or simplify the prompt. |
| Assistant does not respond to wake word | Text input not containing the exact phrase (case‑insensitive) | Speak/type “hey kutti” exactly; the assistant looks for the substring. |

---

## License

This project is provided as‑is for educational and experimental purposes. Feel free to modify and extend it.

---

## Acknowledgments

- **Groq** – for providing fast LLM inference via an OpenAI‑compatible API.  
- **NVIDIA** – for the Nemotron‑3 Super model (alternative endpoint).  
- **Open‑source libraries**: SpeechRecognition, pyttsx3, python‑dotenv, requests, MediaPipe, OpenCV, Three.js.  

--- 

**You now have a working foundation for a JARVIS‑like assistant.  
Add modalities one by one, test thoroughly, and soon you’ll have a truly multimodal, futuristic companion.** 🚀