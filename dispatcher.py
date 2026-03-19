import json
import actions  # Imports the hands we built on Day 17!

def execute_command(json_string):
    """
    Takes a JSON string from the LLM, parses it, and executes the physical action.
    Returns a verbal response for the AI to speak.
    """
    try:
        # 1. Parse the text into a Python Dictionary
        command_data = json.loads(json_string)
        
        task = command_data.get("task", "")
        target = command_data.get("target", "")
        
        print(f"[DISPATCHER] Task Received: '{task}', Target: '{target}'")
        
        # 2. Route to the correct function in actions.py
        if task == "open_app":
            result_msg = actions.open_app(target)
            return result_msg
            
        elif task == "get_time":
            result_msg = actions.get_system_time()
            return result_msg
            
        else:
            return f"Error: Dispatcher does not recognize the task '{task}'."

    except json.JSONDecodeError:
        # If the LLM hallucinates or messes up the JSON formatting
        print("[DISPATCHER ERROR] Invalid JSON format received.")
        return "I'm sorry, my systems encountered a formatting error while trying to do that."
    except Exception as e:
        print(f"[DISPATCHER ERROR] {e}")
        return "I'm sorry, I encountered a critical system error."

# --- TEST BLOCK ---
# This simulates the LLM sending JSON data to the dispatcher
if __name__ == "__main__":
    print("========================================")
    print("   NEURAL KEY: DISPATCHER TEST")
    print("========================================")
    
    # Fake JSON string exactly like what the LLM generated on Day 18
    fake_llm_output_1 = '{"task": "get_time", "target": "none"}'
    fake_llm_output_2 = '{"task": "open_app", "target": "notepad"}'
    
    print("\n[Simulating LLM Output 1]")
    print(f"Executing: {fake_llm_output_1}")
    response_1 = execute_command(fake_llm_output_1)
    print(f"Result to Speak: {response_1}")
    
    print("\n[Simulating LLM Output 2]")
    print(f"Executing: {fake_llm_output_2}")
    response_2 = execute_command(fake_llm_output_2)
    print(f"Result to Speak: {response_2}")


