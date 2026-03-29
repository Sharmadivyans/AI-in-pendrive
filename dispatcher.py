import json
import actions

def execute_command(json_string):
    """
    Takes a JSON string from the LLM, parses it, and safely executes the physical action.
    Returns a verbal response for the AI to speak.
    """
    try:
        # 1. Parse the text into a Python Dictionary
        command_data = json.loads(json_string)
        
        # 2. Extract data safely using .get() to avoid KeyError crashes
        task = command_data.get("task", "")
        target = command_data.get("target", "")
        
        print(f"[DISPATCHER] Task Received: '{task}', Target: '{target}'")
        
        # 3. Route to the correct function in actions.py
        if task == "open_app":
            if not target:
                return "Error: You asked me to open an application, but didn't specify which one."
            
            result_msg = actions.open_app(target)
            return result_msg
            
        elif task == "get_time":
            result_msg = actions.get_system_time()
            return result_msg
            
        else:
            return f"Error: Dispatcher does not recognize the task '{task}'."

    except json.JSONDecodeError:
        # If the LLM hallucinates or messes up the JSON formatting
        print("[DISPATCHER ERROR] Invalid JSON format received from LLM.")
        return "I'm sorry, my neural core encountered a formatting error while trying to process that command."
        
    except Exception as e:
        # Catch-all for any other unforeseen crash (like permission errors)
        print(f"[DISPATCHER CRITICAL ERROR] {e}")
        return f"I'm sorry, I encountered a critical system error: {str(e)}"
