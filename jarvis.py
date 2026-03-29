import sys
import os
import queue
import json
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from llama_cpp import Llama

# UI Library Imports
from rich.console import Console
from rich.panel import Panel

# Ensure Python looks in the current folder for dispatcher/actions
# This must come BEFORE importing local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Local Module Imports
import dispatcher  # Corrected spelling from dispacher
import actions

# Initialize Rich UI Console
console = Console()

# --- DYNAMIC PATHS ---
# Using os.path.dirname(os.path.abspath(__file__)) points to /src
# We go one level up to find /models
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "brain.gguf")
VOSK_PATH = os.path.join(BASE_DIR, "models", "vosk_model")

# --- INITIALIZE VOICE (TTS) ---
tts = pyttsx3.init()
tts.setProperty('rate', 170) 

def speak(text):
    console.print(Panel(f"[bold cyan]{text}[/bold cyan]", title="[bold blue]JARVIS[/bold blue]", border_style="blue", expand=False))
    tts.say(text)
    tts.runAndWait()

# --- INITIALIZE EARS (VOSK) ---
audio_queue = queue.Queue()

def audio_callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    audio_queue.put(bytes(indata))

def main():
    # Clear terminal
    os.system('cls' if os.name == 'nt' else 'clear')
    
    console.print(Panel("[bold yellow]NEURAL KEY: FULL SYSTEM ONLINE[/bold yellow]", border_style="yellow", expand=False))

    # Path verification
    if not os.path.exists(MODEL_PATH):
        console.print(f"[bold red][CRITICAL ERROR] AI Brain missing at: {MODEL_PATH}[/bold red]")
        return
    if not os.path.exists(VOSK_PATH):
        console.print(f"[bold red][CRITICAL ERROR] Vosk Voice Model missing at: {VOSK_PATH}[/bold red]")
        return

    # Loading models
    with console.status("[bold green]Booting Neural Core and Acoustic Models...[/bold green]", spinner="aesthetic"):
        # n_ctx=8192 for deep memory; n_gpu_layers=0 for maximum compatibility across different PCs
        llm = Llama(model_path=MODEL_PATH, n_ctx=8192, n_gpu_layers=0, verbose=False)
        v_model = Model(VOSK_PATH) # Renamed from vosk-model
        recognizer = KaldiRecognizer(v_model, 16000)

    speak("All systems online. I am listening.")

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    user_text = result.get("text", "").lower().strip()
                    
                    if not user_text:
                        continue
                        
                    console.print(f"\n[bold green]YOU:[/bold green] [white]{user_text}[/white]")

                    if "shut down" in user_text or "exit" in user_text:
                        speak("Shutting down systems. Goodbye, sir.")
                        break

                    # Animated spinner while generating
                    with console.status("[bold magenta]Thinking...[/bold magenta]", spinner="dots"):
                        system_prompt = (
                            "You are JARVIS, a sophisticated AI. "
                            "If the user wants to open an app, respond ONLY with: {\"task\": \"open_app\", \"target\": \"name\"}. "
                            "If they ask for time, respond ONLY with: {\"task\": \"get_time\", \"target\": \"none\"}. "
                            "Otherwise, give a brief, helpful spoken response."
                        )
                        
                        prompt = f"System: {system_prompt}\nUser: {user_text}\nAssistant:"
                        
                        response = llm(prompt, max_tokens=150, stop=["User:", "\n"])
                        ai_text = response['choices'][0]['text'].strip()

                    # --- DECISION ENGINE ---
                    if "{" in ai_text and "}" in ai_text:
                        # Use dispatcher to clean and execute the command
                        action_result = dispatcher.execute_command(ai_text)
                        speak(action_result)
                    else:
                        speak(ai_text)
                        
    except KeyboardInterrupt:
        console.print("\n[bold red][SYSTEM] Manual override detected. Offline.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red][ERROR] System crash: {e}[/bold red]")

if __name__ == "__main__":
    main()
