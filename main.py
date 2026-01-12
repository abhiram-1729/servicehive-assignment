import os
from agent import app
from dotenv import load_dotenv

# Set up the environment
load_dotenv()

def main():
    """
    The main CLI loop for interacting with our AutoStream Agent.
    """
    print("--- AutoStream Support Portal ---")
    print("Talk to our AI assistant. Type 'exit' to end the session.")
    
    # Initialize the session state
    state = {
        "messages": [], # List of conversation turns
        "lead_info": {}  # Stores gathered user info
    }
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit", "bye"]:
                print("Closing session. Have a great day!")
                break
            
            # Format the user input for the AI model
            state["messages"].append({"role": "user", "parts": [user_input]})
            
            # Get the processing result from our agent logic
            output = app.invoke(state)
            
            # Update local state with the model's response and history
            state.update(output)
            
            # Pull the latest model response from the history
            latest_msg = state["messages"][-1]
            if latest_msg["role"] == "model":
                print(f"AI: {latest_msg['parts'][0]}")
            else:
                # Fallback in case something unusual happened in the logic
                print("AI: [Thinking... Please try again.]")
                
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\nSession interrupted. Exiting.")
            break
        except Exception as e:
            # Catch and display errors during runtime
            print(f"\nOops! Something went wrong: {e}")

if __name__ == "__main__":
    main()
