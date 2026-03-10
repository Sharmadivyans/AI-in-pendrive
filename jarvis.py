import sys
import os
from llama_cpp import Llama

# Dynamically get paths
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(USB_ROOT, "models", "brain.gguf")

def main():
    print("========================================")
    print("   PORTABLE AI ENVIRONMENT: ACTIVE")
    print("========================================")

    if not os.path.exists(MODEL_PATH):
        print(f"[ERROR] Brain not found at: {MODEL_PATH}")
        return

    print("Loading AI Brain into RAM... Please wait.\n")
    # n_gpu_layers=0 forces CPU mode for maximum portability
    llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_gpu_layers=0, verbose=False)
    print("[SYSTEM] Neural Core Online.\n")

    # First Test Prompt
    prompt = "Q: What is the capital of Japan? A:"
    print(f"Testing Prompt: {prompt}")

    response = llm(prompt, max_tokens=32, stop=["Q:", "\n"])
    print(f"\nAI Response: {response['choices'][0]['text'].strip()}")

if __name__ == "__main__":
    main()