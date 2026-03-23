import sys
import os
import queue
import json
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from llama_cpp import Llama

# Import the custom modules you built!
import dispatcher

# --- DYNAMIC PATHS ---
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")
VOSK_PATH = os.path.join(USB_ROOT, "models", "vosk_model")

# --- INITIALIZE VOICE (TTS) ---
tts = pyttsx3.init()
tts.setProperty('rate', 160)

def speak(text):
    print(f"\nJARVIS: {text}")
    tts.say(text)
    tts.runAndWait()

# --- INITIALIZE EARS (VOSK) ---
audio_queue = queue.Queue()
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def main():
    print("========================================")
    print("   NEURAL KEY: FULL SYSTEM ONLINE")
    print("========================================")

    # 1. System Checks
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VOSK_PATH):
        print("[CRITICAL ERROR] Missing AI or Vosk models in /models directory.")
        return

    print("\n[SYSTEM] Booting Neural Core and Acoustic Models... (Please wait)")
    
    # 2. Load Brain & Ears into RAM
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=0, verbose=False)
    vosk_model = Model(VOSK_PATH)
    recognizer = KaldiRecognizer(vosk_model, 16000)

    speak("All systems online. I am listening.")

    # 3. The Master Loop (Listen -> Think -> Act -> Speak)
    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = audio_queue.get()
                
                # If JARVIS hears a full sentence
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    user_text = result.get("text", "")
                    
                    if user_text.strip() == "":
                        continue
                        
                    print(f"\nYOU SAID: '{user_text}'")

                    # Check for exit command
                    if "shut down" in user_text or "exit" in user_text:
                        speak("Shutting down systems. Goodbye.")
                        break

                    speak("Processing...")

                    # --- THE HYBRID PROMPT ---
                    # This tells the AI to output JSON for commands, and normal text for conversation
                    system_prompt = """You are JARVIS. 
If the user asks to open an app, output strictly JSON: {"task": "open_app", "target": "app name"}.
If the user asks for the time, output strictly JSON: {"task": "get_time", "target": "none"}.
If it is a general question, do NOT use JSON. Answer conversationally in plain text."""
                    
                    prompt = f"System: {system_prompt}\nUser: {user_text}\nAssistant:"
                    
                    # Generate the Brain's response
                    response = llm(prompt, max_tokens=150, stop=["User:", "\n\n"])
                    ai_text = response['choices'][0]['text'].strip()

                    # --- THE DECISION ENGINE ---
                    try:
                        # Try to read the AI's output as JSON (Command Mode)
                        json_command = json.loads(ai_text)
                        if "task" in json_command:
                            # Send to dispatcher and speak the result (e.g., "Successfully opened Calculator")
                            action_result = dispatcher.execute_command(ai_text)
                            speak(action_result)
                    except json.JSONDecodeError:
                        # If it's NOT JSON, the AI just wants to chat! (Conversation Mode)
                        speak(ai_text)
                        
    except KeyboardInterrupt:
        print("\n[SYSTEM] Terminated by user.")
    except Exception as e:
        print(f"\n[ERROR] System crash: {e}")

if __name__ == "__main__":
    main()
