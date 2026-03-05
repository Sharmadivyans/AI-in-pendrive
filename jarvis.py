import sys
import os

# Dynamically get the root path of the USB drive
USB_ROOT = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(USB_ROOT, "models")

def main():
    print("System Booting...")
    print(f"USB Root identified as: {USB_ROOT}")

    # Create the models folder if it doesn't exist yet
    if not os.path.exists(MODELS_DIR):
        os.makedirs(MODELS_DIR)
        print("Created /models directory for Week 2.")
    else:
        print("/models directory already exists. Ready for Week 2!")

if __name__ == "__main__":
    main()

