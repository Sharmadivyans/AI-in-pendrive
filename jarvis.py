import sys
import os
import queue
import json
import pyttsx3
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from llama_cpp import Llama
from rich.console import Console
from rich.panel import Panel
import dispatcher

# Initialize Rich UI Console
console = Console()

# --- DYNAMIC PATHS ---
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")
VOSK_PATH = os.path.join(USB_ROOT, "models", "vosk_model")

# --- INITIALIZE VOICE (TTS) ---
tts = pyttsx3.init()
tts.setProperty('rate', 160)

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
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print(Panel("[bold yellow]NEURAL KEY: FULL SYSTEM ONLINE[/bold yellow]", border_style="yellow", expand=False))

    if not os.path.exists(MODEL_PATH) or not os.path.exists(VOSK_PATH):
        console.print("[bold red][CRITICAL ERROR] Missing AI or Vosk models in /models directory.[/bold red]")
        return

    with console.status("[bold green]Booting Neural Core and Acoustic Models...[/bold green]", spinner="aesthetic"):
        llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=0, verbose=False)
        vosk_model = Model(VOSK_PATH)
        recognizer = KaldiRecognizer(vosk_model, 16000)

    speak("All systems online. I am listening.")

    # --- SHORT TERM MEMORY BUFFER ---
    chat_history = [] 

    try:
        with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                               channels=1, callback=audio_callback):
            while True:
                data = audio_queue.get()
                
                if recognizer.AcceptWaveform(data):
                    result = json.loads(recognizer.Result())
                    user_text = result.get("text", "")
                    
                    if user_text.strip() == "":
                        continue
                        
                    console.print(f"\n[bold green]YOU:[/bold green] [white]{user_text}[/white]")

                    if "shut down" in user_text or "exit" in user_text:
                        speak("Shutting down systems. Goodbye.")
                        break

                    with console.status("[bold magenta]Processing neural response...[/bold magenta]", spinner="dots"):
                        
                        system_prompt = """You are a highly advanced, offline tactical AI framework.
                        Your primary directive is system automation and secure data processing. 
                        Speak concisely, formally, and use technical terminology. Address the user as 'Operator'.
                        If the Operator asks to open an app, output strictly JSON: {"task": "open_app", "target": "app name"}.
                        If the Operator asks for the time, output strictly JSON: {"task": "get_time", "target": "none"}.
                        If it is a general question, do NOT use JSON. Answer conversationally in plain text."""
                        # 1. Start the prompt with the system instructions
                        prompt = f"System: {system_prompt}\n"
                        
                        # 2. Inject the short-term memory (Past conversations)
                        for exchange in chat_history:
                            prompt += f"User: {exchange['user']}\nAssistant: {exchange['ai']}\n"
                            
                        # 3. Add the current question
                        prompt += f"User: {user_text}\nAssistant:"
                        
                        # 4. Generate response
                        response = llm(prompt, max_tokens=150, stop=["User:", "\n\n"])
                        ai_text = response['choices'][0]['text'].strip()

                        # 5. Save this conversation to memory (Keep only the last 3 to save RAM)
                        chat_history.append({"user": user_text, "ai": ai_text})
                        if len(chat_history) > 3:
                            chat_history.pop(0)

                    # Decision Engine
                    try:
                        json_command = json.loads(ai_text)
                        if "task" in json_command:
                            action_result = dispatcher.execute_command(ai_text)
                            speak(action_result)
                    except json.JSONDecodeError:
                        speak(ai_text)
                        
    except KeyboardInterrupt:
        console.print("\n[bold red][SYSTEM] Terminated by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red][ERROR] System crash: {e}[/bold red]")

if __name__ == "__main__":
    main()