import sys
import os
import pyttsx3
from llama_cpp import Llama

# ==============================
# DYNAMIC USB PATHS
# ==============================
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")

# ==============================
# INIT VOICE ENGINE
# ==============================
tts = pyttsx3.init()
tts.setProperty('rate', 160)

def speak(text):
    """Speak text using offline TTS"""
    tts.say(text)
    tts.runAndWait()

def main():
    print("========================================")
    print("   NEURAL KEY: VOICE CORE ACTIVE")
    print("========================================")

    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Brain not found at: {MODEL_PATH}")
        return

    # Wake-up message
    speak("Initializing neural core.")

    # Load AI model
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_gpu_layers=0,
        verbose=False
    )

    print("[SYSTEM] Neural Core Online. Type 'exit' to quit.\n")
    speak("System ready.")

    # ==============================
    # BASIC MEMORY / CHAT HISTORY
    # ==============================
    system_prompt = (
        "You are Neural Key, a portable offline AI assistant running from a USB drive. "
        "You are helpful, concise, futuristic, and slightly JARVIS-like. "
        "Answer clearly and avoid overly long responses."
    )

    conversation_history = f"System: {system_prompt}\n"

    while True:
        user_input = input("\nYou: ")

        # Exit command
        if user_input.lower() in ['exit', 'quit']:
            speak("Shutting down.")
            break

        # Ignore blank input
        if not user_input.strip():
            continue

        # Add user input to history
        conversation_history += f"User: {user_input}\nAssistant:"

        # Generate response
        response = llm(
            conversation_history,
            max_tokens=180,
            temperature=0.7,
            top_p=0.9,
            stop=["User:", "System:"]
        )

        ai_text = response['choices'][0]['text'].strip()

        # Fallback if empty response
        if not ai_text:
            ai_text = "I am online, but I could not generate a response."

        print(f"\nAI: {ai_text}")
        speak(ai_text)

        # Add AI reply to history
        conversation_history += f" {ai_text}\n"

        # Optional: Prevent history from becoming too large
        if len(conversation_history) > 6000:
            conversation_history = (
                f"System: {system_prompt}\n"
                + conversation_history[-4000:]
            )

if __name__ == "__main__":
    main()
