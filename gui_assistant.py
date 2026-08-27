import tkinter as tk
from tkinter import scrolledtext
import threading
import queue
import time
import os
import sys

# Add the current directory to the path so we can import assistant
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from assistant import Assistant

class GuiAssistant:
    def __init__(self):
        self.assistant = Assistant(use_voice=False)  # We'll handle voice ourselves
        self.listen_queue = queue.Queue()
        self.stop_listening = False
        self.is_listening_for_command = False
        
        # Set up GUI
        self.root = tk.Tk()
        self.root.title("Hey Kutti Assistant")
        self.root.geometry("500x600")
        self.root.configure(bg='#1a1a1a')
        
        # Title
        title_label = tk.Label(
            self.root, 
            text="Hey Kutti Assistant", 
            font=("Helvetica", 16, "bold"),
            bg='#1a1a1a',
            fg='#00ff00'
        )
        title_label.pack(pady=10)
        
        # Status indicator (circle)
        self.status_canvas = tk.Canvas(
            self.root, 
            width=60, 
            height=60, 
            bg='#1a1a1a', 
            highlightthickness=0
        )
        self.status_canvas.pack(pady=10)
        self.status_circle = self.status_canvas.create_oval(
            10, 10, 50, 50, 
            fill='#ff0000',  # Red = sleeping
            outline='#00ff00'
        )
        self.status_label = tk.Label(
            self.root, 
            text="Say 'Hey Kutti' to wake me up", 
            font=("Helvetica", 10),
            bg='#1a1a1a',
            fg='#ffffff'
        )
        self.status_label.pack(pady=5)
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(
            self.root, 
            wrap=tk.WORD, 
            width=50, 
            height=20,
            font=("Consolas", 10),
            bg='#2b2b2b',
            fg='#ffffff',
            insertbackground='#ffffff'
        )
        self.chat_display.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)
        self.chat_display.config(state='disabled')
        
        # Start listening thread
        self.listen_thread = threading.Thread(target=self.listen_for_wake_word, daemon=True)
        self.listen_thread.start()
        
        # Check queue for messages from the listening thread
        self.root.after(100, self.process_queue)
        
        # Animation variables
        self.animation_phase = 0
        self.animate_status()
    
    def update_status_circle(self, color, text=None):
        """Update the status circle color and optional text"""
        self.status_canvas.itemconfig(self.status_circle, fill=color)
        if text:
            self.status_label.config(text=text)
    
    def animate_status(self):
        """Animate the status circle when listening"""
        if self.is_listening_for_command:
            # Pulse green when listening for command
            intensity = 128 + 127 * abs(self.animation_phase)
            color = f'#{intensity:02x}ff{intensity:02x}'
            self.update_status_circle(color, "Listening for your command...")
            self.animation_phase = (self.animation_phase + 0.1) % 2
        elif not self.stop_listening:
            # Red when sleeping/waiting for wake word
            self.update_status_circle('#ff0000', "Say 'Hey Kutti' to wake me up")
        
        self.root.after(100, self.animate_status)
    
    def add_to_chat(self, sender, message):
        """Add a message to the chat display"""
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_display.config(state='disabled')
        self.chat_display.see(tk.END)
    
    def listen_for_wake_word(self):
        """Listen for wake word in background thread"""
        import speech_recognition as sr
        
        recognizer = sr.Recognizer()
        microphone = sr.Microphone()
        
        # Adjust for ambient noise
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=1)
        
        while not self.stop_listening:
            try:
                with microphone as source:
                    # Listen for wake word with short timeout
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
                    try:
                        command = recognizer.recognize_google(audio).lower()
                        if "hey kutti" in command:
                            # Wake word detected
                            self.listen_queue.put(("wake_word", None))
                            # Now listen for the actual command
                            self.is_listening_for_command = True
                            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                            command = recognizer.recognize_google(audio).lower()
                            self.listen_queue.put(("command", command))
                            self.is_listening_for_command = False
                    except sr.UnknownValueError:
                        # Didn't understand, continue listening
                        pass
                    except sr.RequestError as e:
                        self.listen_queue.put(("error", f"Could not request results: {e}"))
            except sr.WaitTimeoutError:
                # Timeout, continue listening
                pass
            except Exception as e:
                self.listen_queue.put(("error", f"Error in listening: {str(e)}"))
                break
    
    def process_queue(self):
        """Process messages from the listening thread"""
        try:
            while True:
                msg = self.listen_queue.get_nowait()
                if msg[0] == "wake_word":
                    self.update_status_circle('#ffff00', "Wake word detected! Listening for command...")
                    self.add_to_chat("System", "Wake word detected!")
                elif msg[0] == "command":
                    command = msg[1]
                    self.add_to_chat("You", command)
                    self.process_command(command)
                elif msg[0] == "error":
                    self.add_to_chat("System", f"Error: {msg[1]}")
                    self.update_status_circle('#ff0000', "Error occurred. Say 'Hey Kutti' to try again.")
        except queue.Empty:
            pass
        self.root.after(100, self.process_queue)
    
    def process_command(self, command):
        """Process a command using the assistant"""
        try:
            # Greet the user
            self.assistant.speak("Hello Mr. Vishnu.")
            self.add_to_chat("Assistant", "Hello Mr. Vishnu.")
            
            # Process the command
            self.update_status_circle('#00ffff', "Processing your command...")
            response = self.assistant.process_command(command)
            self.add_to_chat("Assistant", response)
            self.assistant.speak(response)
            
            # Go back to listening for wake word
            self.update_status_circle('#ff0000', "Say 'Hey Kutti' to wake me up")
        except Exception as e:
            self.add_to_chat("System", f"Error processing command: {str(e)}")
            self.update_status_circle('#ff0000', "Error. Say 'Hey Kutti' to try again.")
    
    def run(self):
        """Start the GUI application"""
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()
    
    def on_closing(self):
        """Handle window closing"""
        self.stop_listening = True
        self.root.destroy()

if __name__ == "__main__":
    app = GuiAssistant()
    app.run()