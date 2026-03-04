import sys
import os

def main():
    print("========================================")
    print("   PORTABLE AI ENVIRONMENT: ACTIVE")
    print("========================================")
    
    # Prove it is running from the USB, not the PC
    print(f"\n[SYSTEM] Executable Path: {sys.executable}")
    print(f"[SYSTEM] Current Directory: {os.getcwd()}")
    print("\nIf the path above points to your USB drive, Phase 1 is a SUCCESS!")
    print("You are ready for Week 2 (Intelligence & Inference).")

if __name__ == "__main__":
    main()
