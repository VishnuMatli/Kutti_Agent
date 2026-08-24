import sys
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import platform
import shlex
import shutil
import os
import requests
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

class Assistant:
    def __init__(self, use_voice=False):
        self.use_voice = use_voice
        self.system = platform.system().lower()
        # Try Groq first, then NVIDIA as fallback
        self.api_key = os.getenv("GROQ_API_KEY") or os.getenv("NVIDIA_API_KEY")
        self.api_base = os.getenv("GROQ_API_BASE") or os.getenv("NVIDIA_API_BASE", "https://integrate.api.nvidia.com/v1")
        self.llm_model = os.getenv("GROQ_LLM_MODEL") or os.getenv("NVIDIA_LLM_MODEL", "nvidia/nemotron-3-super-120b-a12b")
        
        # Email credentials from environment
        self.email_user = os.getenv("EMAIL_USER")
        self.email_app_password = os.getenv("EMAIL_APP_PASSWORD")
        self.email_to = os.getenv("EMAIL_TO")
        self.email_subject = os.getenv("EMAIL_SUBJECT")
        self.email_body = os.getenv("EMAIL_BODY")
        
        if use_voice:
            try:
                import speech_recognition as sr
                import pyttsx3
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                self.tts_engine = pyttsx3.init()
                self.tts_engine.setProperty('rate', 150)
                print("Voice capabilities enabled")
            except ImportError as e:
                print(f"Voice dependencies not available: {e}")
                print("Falling back to text mode")
                self.use_voice = False
        else:
            print("Running in text mode")
    
    def speak(self, text):
        """Output text via speech or print"""
        print(f"Assistant: {text}")
        if self.use_voice:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
    
    def listen(self):
        """Get input via voice or text"""
        if self.use_voice:
            with self.microphone as source:
                print("Listening...")
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    command = self.recognizer.recognize_google(audio).lower()
                    print(f"You said: {command}")
                    return command
                except Exception as e:
                    print(f"Voice error: {e}")
                    self.speak("Sorry, I didn't understand that.")
                    return None
        else:
            # Text input mode
            try:
                command = input("You: ").lower().strip()
                return command if command else None
            except KeyboardInterrupt:
                return None
            except EOFError:
                # Handle non-interactive mode
                return None
    
    def query_llm(self, prompt):
        """Send prompt to LLM API (Groq or NVIDIA) via requests and return response"""
        if not self.api_key or self.api_key in ["your_api_key_here", "gsk_your_actual_groq_api_key_here"]:
            return "LLM API key not configured. Please set GROQ_API_KEY or NVIDIA_API_KEY in .env file."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        # Using a simple payload that works with both Groq and NVIDIA endpoints
        payload = {
            "model": self.llm_model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 150
        }
        
        try:
            response = requests.post(f"{self.api_base}/chat/completions", headers=headers, json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()
            # Extract the assistant's message
            return result["choices"][0]["message"]["content"].strip()
        except Exception as e:
            print(f"LLM error: {e}")
            return f"Sorry, I encountered an error: {e}"
    
    def process_wake_word(self, initial_command=None):
        """Handle wake word detection and subsequent interaction"""
        self.speak("Hello Mr. Vishnu.")
        query = None
        if initial_command:
            # Remove the wake word from the initial command
            query = initial_command.replace('hey kutti', '', 1).strip()
        if not query:
            # Listen for user query
            query = self.listen()
        if query:
            # Treat the query as a command; if not recognized, fall back to LLM
            self.process_command(query)
        else:
            self.speak("I didn't catch that.")
    
    def process_command(self, command):
        """Process recognized commands (for text mode or direct commands)"""
        if not command:
            return
        
        print(f"Executing: {command}")
        
        # More flexible command matching: check for keywords
        if 'calculator' in command:
            self.open_calculator()
        elif 'notepad' in command or 'text editor' in command:
            self.open_text_editor()
        elif 'browser' in command or 'web' in command:
            self.open_browser()
        elif 'terminal' in command:
            self.open_terminal()
        elif 'send email' in command or 'email' in command:
            self.send_email()
        elif 'time' in command:
            self.tell_time()
        elif 'date' in command:
            self.tell_date()
        elif 'exit' in command or 'quit' in command or 'goodbye' in command:
            self.speak("Goodbye!")
            sys.exit(0)
        elif 'open' in command:
            # Handle open commands with optional URL and browser
            url = None
            if 'youtube' in command:
                url = 'https://www.youtube.com'
            elif 'google' in command:
                url = 'https://www.google.com'
            # If no specific site, default to google (or could be blank)
            if url is None:
                # fallback to previous behavior (opens google)
                self.open_browser()
                return
            use_chrome = 'chrome' in command
            self.open_url(url, use_chrome)
        else:
            # For any other command, try to use LLM to generate a response
            if self.api_key and self.api_key not in ["your_api_key_here", "gsk_your_actual_groq_api_key_here"]:
                self.speak("Let me think...")
                llm_response = self.query_llm(command)
                self.speak(llm_response)
            else:
                self.speak("I'm not sure how to do that yet. Try saying 'calculator', 'open text editor', 'send email', or 'what time is it'")
    
    def open_url(self, url, use_chrome=False):
        """Open a URL in the specified browser if possible"""
        try:
            if use_chrome:
                # Try to open with Google Chrome specifically
                if self.system == "windows":
                    subprocess.Popen(['start', 'chrome', url], shell=True)
                elif self.system == "darwin":  # macOS
                    subprocess.Popen(['open', '-a', 'Google Chrome', url])
                else:  # Linux and others
                    # Try google-chrome executable
                    if shutil.which('google-chrome'):
                        subprocess.Popen(['google-chrome', url])
                    elif shutil.which('chromium-browser'):
                        subprocess.Popen(['chromium-browser', url])
                    elif shutil.which('chromium'):
                        subprocess.Popen(['chromium', url])
                    else:
                        # Fallback to xdg-open
                        subprocess.Popen(['xdg-open', url])
            else:
                # Default browser
                if self.system == "windows":
                    subprocess.Popen(['start', url], shell=True)
                elif self.system == "darwin":  # macOS
                    subprocess.Popen(['open', url])
                else:  # Linux and others
                    subprocess.Popen(['xdg-open', url])
            self.speak(f"Opening {url}")
        except Exception as e:
            print(f"Error opening URL: {e}")
            self.speak("Sorry, I couldn't open the URL.")
    
    def open_text_editor(self):
        try:
            if self.system == "windows":
                subprocess.Popen(['notepad.exe'])
            elif self.system == "darwin":  # macOS
                subprocess.Popen(['open', '-e'])
            else:  # Linux and others
                # Try common text editors
                for editor in ['gedit', 'kate', 'xed', 'mousepad', 'nano']:
                    if shutil.which(editor):
                        subprocess.Popen([editor])
                        break
                else:
                    # Fallback to xdg-open with a text file
                    subprocess.Popen(['xdg-open', '/tmp/note.txt'])
            self.speak("Opening text editor")
        except Exception as e:
            print(f"Error opening text editor: {e}")
            self.speak("Sorry, I couldn't open the text editor")
    
    def open_calculator(self):
        try:
            if self.system == "windows":
                subprocess.Popen(['calc.exe'])
            elif self.system == "darwin":  # macOS
                subprocess.Popen(['open', '-a', 'Calculator'])
            else:  # Linux and others
                # Try common calculators
                for calc in ['gnome-calculator', 'kcalc', 'galculator', 'xcalc']:
                    if shutil.which(calc):
                        subprocess.Popen([calc])
                        break
                else:
                    self.speak("Sorry, I couldn't find a calculator application")
                    return
            self.speak("Opening Calculator")
        except Exception as e:
            print(f"Error opening calculator: {e}")
            self.speak("Sorry, I couldn't open the calculator")
    
    def open_browser(self):
        # Default to opening Google Chrome if available, else fallback
        self.open_url('https://www.google.com', use_chrome=True)
    
    def open_terminal(self):
        try:
            if self.system == "windows":
                subprocess.Popen(['start', 'cmd'], shell=True)
            elif self.system == "darwin":  # macOS
                subprocess.Popen(['open', '-a', 'Terminal'])
            else:  # Linux and others
                # Try common terminal emulators
                for term in ['gnome-terminal', 'konsole', 'xfce4-terminal', 'lxterminal', 'xterm']:
                    if shutil.which(term):
                        subprocess.Popen([term])
                        break
                else:
                    self.speak("Sorry, I couldn't find a terminal application")
                    return
            self.speak("Opening terminal")
        except Exception as e:
            print(f"Error opening terminal: {e}")
            self.speak("Sorry, I couldn't open the terminal")
    
    def tell_time(self):
        current_time = time.strftime("%I:%M %p")
        self.speak(f"The current time is {current_time}")
    
    def tell_date(self):
        current_date = time.strftime("%A, %B %d, %Y")
        self.speak(f"Today is {current_date}")
    
    def send_email(self):
        """Send a simple email (requires configuration)"""
        # Determine if we are in interactive mode (terminal)
        interactive = sys.stdin.isatty()
        
        self.speak("I'll help you send an email.")
        
        # Get details: if interactive, prompt; else use environment variables
        if interactive:
            to = input(f"To: ") or self.email_to or ""
            if not to:
                to = input("To: ")
            subject = input(f"Subject: ") or self.email_subject or ""
            if not subject:
                subject = input("Subject: ")
            body = input(f"Body: ") or self.email_body or ""
            if not body:
                body = input("Body: ")
            sender_email = self.email_user or input("Your email address: ")
            password = self.email_app_password or input("Your email app password: ")
        else:
            # Non-interactive: rely on environment variables
            to = self.email_to
            subject = self.email_subject
            body = self.email_body
            sender_email = self.email_user
            password = self.email_app_password
            # If any missing, we cannot send
            if not all([to, subject, body, sender_email, password]):
                missing = []
                if not to: missing.append("To (EMAIL_TO)")
                if not subject: missing.append("Subject (EMAIL_SUBJECT)")
                if not body: missing.append("Body (EMAIL_BODY)")
                if not sender_email: missing.append("From (EMAIL_USER)")
                if not password: missing.append("Password (EMAIL_APP_PASSWORD)")
                self.speak(f"Email sending skipped: missing {', '.join(missing)}. Set these in .env or run in interactive mode.")
                return
        
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, to, text)
            server.quit()
            
            self.speak("Email sent successfully")
        except Exception as e:
            print(f"Email error: {e}")
            self.speak("Sorry, I couldn't send the email. Please check your email configuration.")

    def run(self):
        """Main loop for the assistant"""
        self.speak("Assistant initialized. Waiting for wake word 'Hey Kutti'...")
        
        try:
            while True:
                if self.use_voice:
                    command = self.listen()
                    # Check for wake word
                    if command and 'hey kutti' in command:
                        self.process_wake_word(command)
                    # In voice mode, ignore other commands (could prompt to say wake word)
                else:
                    # Text mode: treat any command containing wake word as wake word, else as normal command
                    command = self.listen()
                    if command and 'hey kutti' in command:
                        self.process_wake_word(command)
                    else:
                        self.process_command(command)
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        except KeyboardInterrupt:
            self.speak("Goodbye!")
            print("\nAssistant stopped.")

if __name__ == "__main__":
    # Start in text mode by default - change to True to test voice when dependencies work
    assistant = Assistant(use_voice=False)
    assistant.run()