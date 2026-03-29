import os
import datetime

def get_system_time():
    now = datetime.datetime.now()
    return f"The current system time is {now.strftime('%I:%M %p')}."

def open_app(app_name):
    # Add your logic to find common apps here
    try:
        os.system(f"start {app_name}")
        return f"Opening {app_name} now, sir."
    except:
        return f"I was unable to locate the path for {app_name} on this host machine."
