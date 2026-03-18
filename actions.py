import os
import subprocess
import datetime
import platform

def open_app(app_name):
    """Launches standard Windows applications."""
    app_name = app_name.lower()
    print(f"[ACTION] Attempting to open: {app_name}")
    
    try:
        if "chrome" in app_name or "browser" in app_name:
            os.system("start chrome")
            return "Google Chrome launched successfully."
            
        elif "notepad" in app_name or "text" in app_name:
            subprocess.Popen("notepad.exe")
            return "Notepad opened."
            
        elif "calculator" in app_name or "calc" in app_name:
            subprocess.Popen("calc.exe")
            return "Calculator opened."
            
        elif "explorer" in app_name or "files" in app_name or "folder" in app_name:
            subprocess.Popen("explorer.exe")
            return "File Explorer opened."
            
        else:
            return f"Sorry, I do not have the system path to open {app_name}."
            
    except Exception as e:
        return f"System error while trying to open {app_name}: {e}"

def get_system_status():
    """Returns the current time and OS information."""
    now = datetime.datetime.now().strftime("%I:%M %p")
    date = datetime.datetime.now().strftime("%A, %B %d")
    os_info = f"{platform.system()} {platform.release()}"
    
    status = f"System is currently running {os_info}. The time is {now} on {date}."
    print(f"[ACTION] Status requested: {status}")
    return status

# --- STANDALONE TEST BLOCK ---
# This only runs if you execute actions.py directly, not if jarvis.py imports it.
if __name__ == "__main__":
    print("========================================")
    print("   NEURAL KEY: ACTION MODULE TEST")
    print("========================================")
    
    print("\n1. Testing System Status:")
    print(get_system_status())
    
    print("\n2. Testing App Launch (Opening Calculator...):")
    result = open_app("calc")
    print(result)
