import json
from typing import TypedDict, List, Dict, Optional

# Constants
KNOWLEDGE_BASE_PATH = "knowledge_base.json"

class AgentState(TypedDict):
    messages: List[Dict[str, str]]
    lead_info: Dict[str, str]

def load_knowledge_base():
    with open(KNOWLEDGE_BASE_PATH, "r") as f:
        return json.load(f)

kb_data = load_knowledge_base()

def mock_get_chat_response(state: AgentState):
    """
    Mocked response logic to verify state handling and flow.
    """
    last_msg = state["messages"][-1]["parts"][0].lower()
    response_text = ""
    
    if "hi" in last_msg or "hello" in last_msg:
        response_text = "Hello! I'm AutoStream's assistant. How can I help you today?"
    elif "pricing" in last_msg or "plan" in last_msg:
        response_text = f"We have multiple plans: {json.dumps(kb_data['pricing'])}"
    elif "youtube" in last_msg or "sign up" in last_msg:
        response_text = "I'd love to help! Can you provide your name, email, and platform?"
    elif "@" in last_msg:
        response_text = "Great, I've captured your details!"
    else:
        response_text = "I'm not sure I understand, but I'm here to help with AutoStream!"

    new_messages = state["messages"] + [{"role": "model", "parts": [response_text]}]
    return {
        "messages": new_messages,
        "lead_info": state["lead_info"]
    }

class MockApp:
    def invoke(self, state):
        return mock_get_chat_response(state)

def test_mock_flow():
    app = MockApp()
    state = {"messages": [], "lead_info": {}}

    def run_step(prompt):
        print(f"\nUser: {prompt}")
        state["messages"].append({"role": "user", "parts": [prompt]})
        output = app.invoke(state)
        state.update(output)
        print(f"Agent: {state['messages'][-1]['parts'][0]}")

    print("--- Running Mock Verification ---")
    run_step("Hi!")
    run_step("Tell me about pricing")
    run_step("I want to sign up for my YouTube channel")
    run_step("I'm Abhiram, abhiram@example.com")
    print("\nMock Verification Successful: Logic and state handling passed.")

if __name__ == "__main__":
    test_mock_flow()
