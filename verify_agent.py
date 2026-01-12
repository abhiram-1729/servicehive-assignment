import os
from agent import app
from dotenv import load_dotenv

# Load configuration for testing
load_dotenv()

def run_automated_test_suite():
    """
    A sequence of scripted interactions to verify the agent's behavior 
    across greetings, product knowledge, and lead capture.
    """
    # Start with a clean state for the test
    state = {"messages": [], "lead_info": {}}

    def simulate_turn(prompt):
        """
        Helper to simulate a single user message and display the agent's response.
        """
        print(f"\nUser: {prompt}")
        state["messages"].append({"role": "user", "parts": [prompt]})
        
        # Invoke the agent logic
        output = app.invoke(state)
        
        # Sync state and print result
        state.update(output)
        last_msg = state["messages"][-1]
        
        if last_msg["role"] == "model":
            print(f"Agent: {last_msg['parts'][0]}")
        return output

    print("--- Starting Automated Verification ---")

    # Step 1: Initial Greeting
    print("\n[Phase 1: Basic Greeting]")
    simulate_turn("Hi there!")

    # Step 2: Product Knowledge (RAG)
    print("\n[Phase 2: Product Inquiry]")
    simulate_turn("Can you tell me how much the Pro plan costs?")

    # Step 3: Intent Identification
    print("\n[Phase 3: High-Intent Lead Generation]")
    simulate_turn("That sounds good. I'd like to sign up for my YouTube channel.")

    # Step 4: Multi-turn Lead Collection
    print("\n[Phase 4: Data Collection & Tool Call]")
    simulate_turn("I'm Abhiram, you can reach me at abhiram@example.com.")

    print("\n--- Test Suite Completed Successfully ---")

if __name__ == "__main__":
    # Check for the API key before starting
    if not os.environ.get("GOOGLE_API_KEY"):
        print("CRITICAL ERROR: GOOGLE_API_KEY environment variable is missing.")
    else:
        run_automated_test_suite()
