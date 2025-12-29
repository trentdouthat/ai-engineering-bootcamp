import os
from dotenv import load_dotenv
load_dotenv()



# 1. Import the Google Gemini wrapper
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Setup the "Brain"
# Replace 'AIza...' with your actual Google AI Studio key
llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GOOGLE_API_KEY"), 
    model="gemini-flash-latest"
)

# 3. Send a message to the AI
try:
    response = llm.invoke("Explain what a System Reliability Engineer (SRE) does in one sentence.")
    print("--- GEMINI SAYS ---")
    print(response.content)
except Exception as e:
    print(f"Error: {e}")


# C:\Users\trent\AppData\Local\Microsoft\WindowsApps\python.exe -m pip install langchain-google-genai langchain langchain-community

