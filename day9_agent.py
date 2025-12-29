import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent

# 1. Setup the Brain
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

llm = ChatGoogleGenerativeAI(
    google_api_key=api_key, 
    model=model_name
)

# 2. Define the Tool (Same as before)
@tool
def check_server_status(hostname: str) -> str:
    """Checks the health status of a specific server hostname."""
    mock_db = {
        "web-01": "ONLINE (Load: 15%)",
        "db-01": "CRITICAL (Load: 99%)",
        "cache-01": "OFFLINE"
    }
    return mock_db.get(hostname, "Server not found.")

# 3. Create the Toolkit
tools = [check_server_status]

# 4. Create the Agent (The "Modern" Way)
# "create_react_agent" builds a graph that loops automatically
agent_executor = create_agent(llm,tools)

# 5. Run the Agent
print("--- TEST 1: Asking a question that REQUIRES a tool ---")
# LangGraph expects messages, but we can pass a simple string
response = agent_executor.invoke({"messages": [("user", "Is the database server db-01 healthy right now?")]})

# The response format is slightly different (it's a list of messages)
# We want the LAST message, which is the AI's final answer.
print(f"Final Answer: {response['messages'][-1].content}\n")

print("--- TEST 2: Asking a question that needs NO tools ---")
response = agent_executor.invoke({"messages": [("user", "Write a 1-sentence haiku about Linux.")]})
print(f"Final Answer: {response['messages'][-1].content}")