import sys
import os
from llama_cpp import Llama

# --- DYNAMIC PATHS ---
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")

def main():
    print("========================================")
    print("   NEURAL KEY: JSON BRAIN TRAINING")
    print("========================================")

    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Brain not found at: {MODEL_PATH}")
        return

    print("\n[SYSTEM] Loading AI Brain... (Please wait)")
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=0, verbose=False)

    # THE MAGIC: This strict system prompt forces the AI to output computer code instead of human text.
    system_prompt = """You are a local system controller. 
If the user asks to open or launch an application, output ONLY valid JSON in this exact format: {"task": "open_app", "target": "app_name"}
If the user asks for the time, output ONLY: {"task": "get_time", "target": "none"}
Do not output any other text, no markdown, and no explanations. Just the raw JSON object."""

    # We pretend the user spoke this command
    user_query = "Hey JARVIS, can you open the calculator for me?"
    
    # Combine it into the final prompt sent to the LLM
    prompt = f"System: {system_prompt}\nUser: {user_query}\nAssistant:"
    
    print(f"\nUser asked: '{user_query}'")
    print("AI is translating request into JSON...\n")
    
    # Generate response
    response = llm(prompt, max_tokens=50, stop=["User:", "\n\n"])
    ai_text = response['choices'][0]['text'].strip()
    
    print("================ RAW AI OUTPUT ================")
    print(ai_text)
    print("===============================================")
    
    print("\nIf the output above looks exactly like {\"task\": \"open_app\", \"target\": \"calculator\"}")
    print("Then the Brain Training is a MASSIVE SUCCESS!")

if __name__ == "__main__":
    main()
