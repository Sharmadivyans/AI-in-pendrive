import os
import sys
import queue
import json
import sounddevice as sd
from vosk import Model, KaldiRecognizer

# --- DYNAMIC PATHS ---
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "vosk_model")

# Queue to hold audio data
audio_queue = queue.Queue()

# Callback function to grab audio from the microphone
def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def main():
    print("========================================")
    print("   NEURAL KEY: AUDIO CALIBRATION")
    print("========================================")

    if not os.path.exists(MODEL_PATH):
        print(f"\n[CRITICAL ERROR] Vosk model not found at: {MODEL_PATH}")
        print("Did you extract the model and name the folder 'vosk_model'?")
        return

    print("\n[SYSTEM] Loading offline acoustic model... (Please wait)")
    
    try:
        # Load Vosk Model
        model = Model(MODEL_PATH)
        # Set sample rate to 16000 Hz (standard for Vosk)
        recognizer = KaldiRecognizer(model, 16000)
    except Exception as e:
        print(f"\n[ERROR] Failed to load model: {e}")
        return

    print("\n[SYSTEM] Microphone Active. Speak now... (Press Ctrl+C to stop)")
    
    try:
        # Open the microphone stream
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = audio_queue.get()
                
                # If Vosk detects a completed phrase
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    recognized_text = result.get("text", "")
                    
                    if recognized_text.strip():
                        print(f"JARVIS Heard: {recognized_text}")
                        
    except KeyboardInterrupt:
        print("\n[SYSTEM] Audio calibration terminated by user.")
    except Exception as e:
        print(f"\n[ERROR] Microphone access failed: {e}")

if __name__ == "__main__":
    main()
