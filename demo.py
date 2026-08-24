"""
Demo script showing how the assistant would process commands
This works in non-interactive environments
"""

import sys
import time
from assistant import Assistant

def demo_text_mode():
    """Demonstrate the assistant in text mode with simulated inputs"""
    print("=== Assistant Demo (Text Mode) ===")
    print("Initializing assistant...")
    
    # Create assistant in text mode
    assistant = Assistant(use_voice=False)
    
    # Test commands that don't require interactive input
    test_commands = [
        "what time is it",
        "what is the date",
        "open browser",
        "open text editor",
        "open calculator",
        "open terminal",
        "send email",  # This will show non-interactive handling
        "exit"
    ]
    
    print("\nTesting commands:")
    for i, command in enumerate(test_commands, 1):
        print(f"\n{i}. User: {command}")
        # Instead of using listen(), we'll directly call execute_action
        # In a real scenario, process_command would handle wake words, etc.
        assistant.execute_action(command)
        time.sleep(0.5)  # Small delay between commands
    
    print("\n=== Demo Complete ===")

def demo_voice_mode_simulation():
    """Simulate how voice mode would work"""
    print("\n=== Assistant Demo (Voice Mode Simulation) ===")
    print("In voice mode, the assistant would:")
    print("1. Continuously listen for wake word 'Assistant'")
    print("2. When detected, listen for a command")
    print("3. Process the command using the same execute_action logic")
    print("4. Respond with speech feedback")
    print("\nExample voice interaction:")
    print("User: Assistant, open browser")
    print("Assistant: Yes? (after wake word)")
    print("User: Open browser")
    print("Assistant: Opening web browser")
    print("(Then would actually open the browser)")

if __name__ == "__main__":
    demo_text_mode()
    demo_voice_mode_simulation()
    print("\nNote: To run the full interactive version, you would:")
    print("1. Install dependencies: pip install SpeechRecognition pyttsx3 pyaudio")
    print("2. Install system dependency: sudo apt install portaudio19-dev")
    print("3. Run: python assistant.py")
    print("4. Speak commands starting with 'Assistant' wake word")
    print("\nThe assistant is designed to be cross-platform and will adapt")
    print("to Windows, macOS, or Linux for opening applications.")