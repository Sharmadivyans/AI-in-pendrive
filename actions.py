import os
import subprocess
from datetime import datetime

def open_app(app_name):
    """
    Attempts to open common Windows applications.
    You can easily expand this list to add more capabilities to JARVIS!
    """
    app_name = app_name.lower().strip()
    
    try:
        # Web Browsers
        if "chrome" in app_name:
            os.system("start chrome")
            return "Successfully opened Google Chrome."
        elif "edge" in app_name:
            os.system("start msedge")
            return "Successfully opened Microsoft Edge."
            
        # Utilities
        elif "notepad" in app_name or "notes" in app_name:
            subprocess.Popen("notepad.exe")
            return "Successfully opened Notepad."
        elif "calc" in app_name or "calculator" in app_name:
            subprocess.Popen("calc.exe")
            return "Successfully opened the Calculator."
        elif "explorer" in app_name or "files" in app_name or "folder" in app_name:
            subprocess.Popen("explorer.exe")
            return "Successfully opened File Explorer."
            
        # Office Apps
        elif "word" in app_name:
            os.system("start winword")
            return "Successfully opened Microsoft Word."
            
        else:
            return f"I'm sorry, I do not have the protocol to open '{app_name}' yet."
            
    except Exception as e:
        return f"System error while trying to open the application: {str(e)}"

def get_system_time():
    """Returns the current system time in a conversational format."""
    now = datetime.now()
    current_time = now.strftime("%I:%M %p") 
    return f"The current system time is {current_time}."
