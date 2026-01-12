# AutoStream: AI-Powered Social-to-Lead Agent

AutoStream is an intelligent assistant designed for a fictional video editing SaaS. It converts casual social media conversations into qualified business leads by identifying intent, answering product questions using a knowledge base (RAG), and capturing lead details through multi-turn dialogue.

##  Key Features

- **Native Gemini Integration**: Leveraging the latest Google Gemini 2.5 Flash model for high-performance reasoning.
- **RAG-Powered FAQ**: Answers questions about pricing, plans, and policies using a local JSON knowledge base.
- **Stateful Conversation**: Maintains context across multiple turns to collect user details (Name, Email, Platform).
- **Function Calling**: Automatically triggers a lead capture tool once all required information is gathered.
- **Professional Architecture**: Clean separation between agent logic, tools, and the main interaction loop.

##  Project Structure

- `agent.py`: Core logic for the Gemini model, system instructions, and tool handling.
- `main.py`: Interactive CLI tool for chatting with the agent.
- `tools.py`: Contains the `mock_lead_capture` function for CRM integration.
- `knowledge_base.json`: Local storage for plans, pricing, and company policies.
- `verify_agent.py`: Automated test suite for validating conversation flows.

##  Setup & Installation

1. **Clone the project** and navigate to the directory.
2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Configure Environment**:
   - Create a `.env` file based on `.env_example`.
   - Add your Google AI Studio API key:
     ```env
     GOOGLE_API_KEY=your_actual_key_here
     ```

##  Testing the Agent

### Automated Validation
Run the scripted test suite to verify all core features (Greeting → FAQ → Lead Capture):
```bash
python3 verify_agent.py
```

### Interactive Chat
Talk to the agent directly in your terminal:
```bash
python3 main.py
```

##  Architecture Rationale

This project initially used LangGraph but was migrated to the **native Google Gemini SDK** to reduce overhead and gain finer control over **System Instructions** and **Native Tool Calling**. 

By using Gemini's native state management and function calling, the agent is more robust at handling edge cases during data collection while maintaining a fast, lower-latency response profile.

## 📱 WhatsApp Integration Plan (My Assumption)

we can  deploy this agent on WhatsApp, I would:
1. **Meta Developer Portal**: Set up a WhatsApp Business API account.
2. **FastAPI Webhook**: Build a backend to receive incoming messages from Meta's webhooks.
3. **Context Persistence**: Use a database (like Redis or Supabase) to store conversation history keyed by the user's phone number.
4. **Response Loop**: Forward incoming text to the `AgentApp`, then send the model's response back using the WhatsApp Cloud API.
5. **Async Processing**: Use Celery/Redis to handle requests asynchronously, ensuring responses stay within WhatsApp's 10-second webhook window.
