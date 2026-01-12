import json
import os
import google.generativeai as genai
from typing import TypedDict, List, Dict, Optional
from tools import mock_lead_capture
from dotenv import load_dotenv

# Load API keys and other environment variables
load_dotenv()

# Path to the local FAQ/Knowledge base
KNOWLEDGE_BASE_PATH = "knowledge_base.json"

class AgentState(TypedDict):
    """
    Keep track of the conversation state and any lead info we've gathered.
    """
    messages: List[Dict[str, str]]
    intent: Optional[str]
    lead_info: Dict[str, str]

def load_knowledge_base():
    """
    Helper to pull in our product info from the JSON file.
    """
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return {"pricing": [], "policies": []}
    with open(KNOWLEDGE_BASE_PATH, "r") as f:
        return json.load(f)

# Cache the knowledge base data
kb_data = load_knowledge_base()

# Configure the Gemini SDK
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

def get_chat_response(state: AgentState):
    """
    Core function that talks to Gemini. It handles the system prompt, 
    context injection, and tool calling for lead capture.
    """
    # Preparing the knowledge base context for the model
    kb_context = f"Pricing: {json.dumps(kb_data['pricing'], indent=2)}\nPolicies: {json.dumps(kb_data['policies'], indent=2)}"
    
    # Defining the assistant's behavior and the available data
    system_instruction = f"""
    You are AutoStream's AI assistant. AutoStream is a SaaS for automated video editing.
    
    Guidelines:
    1. Warmly greet users when they reach out.
    2. Use the following Knowledge Base to answer questions about pricing and our policies:
    {kb_context}
    If the answer isn't here, politely direct them to our 24/7 support (available on the Pro plan).
    3. If someone wants to sign up or try a plan, we need their Name, Email, and Creator Platform.
    4. Once you have those 3 pieces of info, trigger the `mock_lead_capture` tool.
    
    Lead Info Status: {json.dumps(state['lead_info'])}
    
    Stay professional, helpful, and concise.
    """

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", # Using the stable flash model for quick responses
        system_instruction=system_instruction,
        tools=[mock_lead_capture]
    )

    # We start the chat session with the message history
    chat = model.start_chat(history=state['messages'][:-1])
    
    # Process the latest message from the user
    last_user_msg = state['messages'][-1]['parts'][0]
    response = chat.send_message(last_user_msg)

    # Check if the model wants to call our lead capture tool
    if response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if fn := part.function_call:
                # Map arguments and execute the mock tool
                tool_args = {arg: val for arg, val in fn.args.items()}
                result = mock_lead_capture(**tool_args)
                
                # Report back to the model that the tool finished successfully
                response = chat.send_message({
                    "parts": [{
                        "function_response": {
                            "name": fn.name,
                            "response": {"result": result}
                        }
                    }]
                })

    # Sync up our state with the latest chat history
    new_history = []
    for content in chat.history:
        role = "user" if content.role == "user" else "model"
        parts = [p.text for p in content.parts if p.text]
        if parts:
            new_history.append({"role": role, "parts": parts})
    
    return {
        "messages": new_history,
        "lead_info": state['lead_info']
    }

class AgentApp:
    """
    Simple wrapper to match the interface used by the main loop.
    """
    def invoke(self, state):
        return get_chat_response(state)

app = AgentApp()
