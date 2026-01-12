# AutoStream Social-to-Lead Agent

An AI-powered platform that converts social media conversations into qualified business leads for AutoStream, an automated video editing SaaS.

## Features
- **Intent Identification**: Classifies user messages into Casual Greeting, Product Inquiry, or High-Intent.
- **RAG-Powered Knowledge Retrieval**: Answers pricing and policy questions using a local JSON knowledge base.
- **Stateful Lead Capture**: Collects name, email, and creator platform across multiple conversation turns.
- **Mock Tool Execution**: Triggers a lead capture function once all data is collected.

## How to Run Locally

1. **Clone the repository** (if applicable).
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Set up your Gemini API Key**:
   ```bash
   export GOOGLE_API_KEY='your_api_key_here'
   ```
4. **Run the agent**:
   ```bash
   python3 main.py
   ```

## Architecture Explanation

I chose **LangGraph** for this project because it excels at managing stateful, cyclic workflows. Unlike linear chains, LangGraph allows the agent to loop back and ask for missing information, which is critical for the lead collection process.

**State Management**: 
The `AgentState` is a `TypedDict` that stores:
- `messages`: A list of all conversation history, ensuring the agent retains context across 5-6 turns.
- `intent`: The current identified user intent, used for routing.
- `lead_info`: A dictionary that accumulates user details (name, email, platform) as they are extracted from different turns.
- `last_requested`: Keeps track of what the agent last asked the user.

The workflow uses a **Classifier Node** to route inputs to specialized nodes: `greeting`, `rag` (for retrieval), or `collector` (for stateful lead capture). This modular approach ensures clean separation of concerns and high reliability in intent detection.

## WhatsApp Deployment

To integrate this agent with WhatsApp, I would use the following steps:

1. **Meta for Developers Account**: Register an app on the Meta developer portal.
2. **Webhook Setup**: Create a FastAPI or Flask endpoint that Meta's servers will call whenever a message is received.
3. **Integration**:
   - Receive the JSON payload from the WhatsApp Cloud API webhook.
   - Extract the `from` phone number (to use as a thread ID for state management) and the message body.
   - Pass the message to the LangGraph `app.invoke()` method, using the phone number to retrieve/persist the state.
   - Send the result back to the user via the WhatsApp Cloud API POST request (`/messages` endpoint).
4. **Asynchronous Handling**: Use a task queue like Celery or a serverless function (AWS Lambda/Vercel) to handle requests asynchronously to avoid timeout issues with WhatsApp's 10-second webhook limit.
