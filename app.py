from flask import Flask, render_template, request, jsonify
import json
import threading
import time
import os
import sys
from assistant import Assistant

app = Flask(__name__)

# Global assistant instance
assistant_instance = None
assistant_lock = threading.Lock()
last_command = ""
last_response = ""
is_listening = False

def initialize_assistant():
    global assistant_instance
    with assistant_lock:
        if assistant_instance is None:
            assistant_instance = Assistant(use_voice=False)  # We'll handle voice separately
            print("Assistant initialized")

def get_assistant():
    global assistant_instance
    with assistant_lock:
        if assistant_instance is None:
            initialize_assistant()
        return assistant_instance

@app.route('/')
def index():
    return render_template('jarvis.html')

@app.route('/process_command', methods=['POST'])
def process_command():
    global last_command, last_response
    data = request.get_json()
    command = data.get('command', '').lower().strip()
    
    if not command:
        return jsonify({'error': 'No command provided'}), 400
    
    last_command = command
    
    try:
        # Get assistant instance
        assistant = get_assistant()
        
        # Process the command using the assistant's logic
        # We'll simulate the wake word detection since we're getting direct commands
        if 'hey kutti' in command:
            # Remove wake word and process
            actual_command = command.replace('hey kutti', '', 1).strip()
            if actual_command:
                response = assistant.process_command(actual_command)
            else:
                response = "Hello Mr. Vishnu. How can I assist you?"
        else:
            # Process as direct command
            response = assistant.process_command(command)
        
        last_response = response
        return jsonify({
            'command': command,
            'response': response,
            'status': 'success'
        })
    except Exception as e:
        print(f"Error processing command: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_status')
def get_status():
    return jsonify({
        'last_command': last_command,
        'last_response': last_response,
        'is_listening': is_listening,
        'timestamp': time.time()
    })

@app.route('/start_listening', methods=['POST'])
def start_listening():
    global is_listening
    is_listening = True
    return jsonify({'status': 'listening started'})

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    global is_listening
    is_listening = False
    return jsonify({'status': 'listening stopped'})

if __name__ == '__main__':
    # Initialize assistant on startup
    initialize_assistant()
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)