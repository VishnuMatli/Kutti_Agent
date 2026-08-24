import speech_recognition as sr
import pyttsx3
import threading
import time
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class VoiceAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        print("Voice Assistant initialized. Say 'Assistant' to wake up.")
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"Assistant: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for audio input and convert to text"""
        with self.microphone as source:
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = self.recognizer.recognize_google(audio).lower()
                print(f"You said: {command}")
                return command
            except sr.WaitTimeoutError:
                return None
            except sr.UnknownValueError:
                self.speak("Sorry, I didn't understand that.")
                return None
            except sr.RequestError:
                self.speak("Sorry, my speech service is down.")
                return None
    
    def process_command(self, command):
        """Process recognized commands"""
        if not command:
            return
        
        if 'assistant' in command:
            # Remove wake word for cleaner command processing
            command = command.replace('assistant', '').strip()
            self.speak("Yes?")
            
            # Listen for actual command
            audio_command = self.listen()
            if audio_command:
                self.execute_action(audio_command)
    
    def execute_action(self, command):
        """Execute specific actions based on command"""
        print(f"Executing: {command}")
        
        if 'open' in command:
            if 'notepad' in command:
                subprocess.Popen(['notepad.exe'])
                self.speak("Opening Notepad")
            elif 'calculator' in command:
                subprocess.Popen(['calc.exe'])
                self.speak("Opening Calculator")
            else:
                self.speak("I can open Notepad or Calculator for now")
        
        elif 'send email' in command:
            self.send_email()
        
        elif 'time' in command:
            current_time = time.strftime("%H:%M")
            self.speak(f"The current time is {current_time}")
        
        else:
            self.speak("I'm not sure how to do that yet. Try saying 'open notepad' or 'send email'")
    
    def send_email(self):
        """Send a simple email (requires configuration)"""
        self.speak("I'll help you send an email. What should I say?")
        
        # In a real implementation, you'd want to get recipient, subject, body via voice
        # For now, using placeholders
        try:
            # Email configuration - USER NEEDS TO FILL THESE IN
            sender_email = "your_email@example.com"
            receiver_email = "receiver@example.com"
            password = "your_app_password"  # Use app password for Gmail
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = receiver_email
            msg['Subject'] = "Test Email from Voice Assistant"
            
            body = "This is a test email sent by your voice assistant."
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            
            self.speak("Email sent successfully")
        except Exception as e:
            print(f"Email error: {e}")
            self.speak("Sorry, I couldn't send the email. Please check your email configuration.")
    
    def run(self):
        """Main loop for the voice assistant"""
        try:
            while True:
                command = self.listen()
                self.process_command(command)
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
        except KeyboardInterrupt:
            self.speak("Goodbye!")
            print("\nAssistant stopped.")

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()