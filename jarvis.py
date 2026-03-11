import sys
import os
from llama_cpp import Llama

# Dynamically get paths
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")

def main():
    print("========================================")
    print("   NEURAL KEY: INTERACTIVE MODE")
    print("========================================")

    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Brain not found at: {MODEL_PATH}")
        return

    # Load the AI Brain
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=0, verbose=False)
    print("[SYSTEM] Neural Core Online. Type 'exit' to quit.\n")

    # The Chat Loop
    while True:
        user_input = input("\nYou: ")
        
        # Check if user wants to quit
        if user_input.lower() in ['exit', 'quit']:
            print("Shutting down Neural Core...")
            break
            
        # Ignore empty inputs
        if user_input.strip() == "":
            continue

        print("AI is thinking...")
        
        # Format the prompt for a conversation
        prompt = f"User: {user_input}\nAssistant:"
        
        # Generate the response
        response = llm(prompt, max_tokens=150, stop=["User:", "\n\n"])
        
        # Extract and print the AI's text
        ai_text = response['choices'][0]['text'].strip()
        print(f"\nAI: {ai_text}")

if __name__ == "__main__":
    main()