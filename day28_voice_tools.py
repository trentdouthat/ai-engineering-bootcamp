import os
import time
import random
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent # <--- The Modern Way

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# Initialize Audio
r = sr.Recognizer()
pygame.mixer.init()

# --- 2. DEFINE TOOLS ---

@tool
def check_server_health(service_name: str):
    """Checks the health status of a specific server or service."""
    print(f"\n[TOOL] Checking status for: {service_name}...")
    time.sleep(1) 
    statuses = ["Online", "Online", "Online", "Overheating", "Disk Full"]
    status = random.choice(statuses)
    return f"The status of {service_name} is: {status}"

tools = [check_server_health]

# --- 3. BUILD AGENT (The LangGraph Way) ---

# This replaces the entire AgentExecutor block
agent_executor = create_react_agent(llm, tools)

# --- 4. AUDIO FUNCTIONS ---

def speak(text):
    print(f"🤖 AI: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp_voice_tool.mp3"
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Audio Error: {e}")

def listen():
    with sr.Microphone() as source:
        print("\n🎤 Listening... (Say 'Check the Database' or 'Exit')")
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

# --- 5. MAIN LOOP ---

def main():
    speak("System Online. Which server should I check?")
    
    while True:
        user_text = listen()
        
        if user_text:
            if "exit" in user_text.lower() or "stop" in user_text.lower():
                speak("Signing off.")
                break
            
            # Run the Agent (LangGraph Style)
            try:
                inputs = {"messages": [HumanMessage(content=user_text)]}
                response = agent_executor.invoke(inputs)
                
                # Get the raw content
                raw_content = response["messages"][-1].content
                
                # FIX: Handle Gemini's structured output
                if isinstance(raw_content, list):
                    # If it's a list, grab the text from the first item
                    final_answer = raw_content[0].get("text", "")
                else:
                    # If it's already a string, use it directly
                    final_answer = raw_content

                speak(final_answer)
                
            except Exception as e:
                print(f"Agent Error: {e}")
                speak("I encountered an error processing that request.")

if __name__ == "__main__":
    main()