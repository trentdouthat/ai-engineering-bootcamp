import os
import time
import random
import sys
import speech_recognition as sr
from gtts import gTTS
import pygame
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent

# 1. Setup & Config
# Suppress the specific warning about deprecation
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite") # Hardcoded to your working model
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# Initialize Audio
r = sr.Recognizer()
r.dynamic_energy_threshold = False # Prevents background noise from adjusting sensitivity too much
r.energy_threshold = 400 # Higher = less sensitive to quiet noise
pygame.mixer.init()

# --- 2. DEFINE TOOLS ---

@tool
def check_server_health(service_name: str):
    """Checks the health status of a specific server or service."""
    # We use sys.stdout.write to update line without newline spam
    print(f"\n[⚡ TOOL] Pinging {service_name}...", end="\r")
    time.sleep(1.5) 
    statuses = ["Online 🟢", "Online 🟢", "Degraded 🟡", "Critical 🔴", "Maintenance 🔵"]
    status = random.choice(statuses)
    print(f"[⚡ TOOL] {service_name}: {status}          ") # Spaces clear the line
    return f"The status of {service_name} is: {status}"

tools = [check_server_health]

# --- 3. BUILD AGENT ---
agent_executor = create_react_agent(llm, tools)

# --- 4. HELPERS ---

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("=========================================")
    print("🎙️  SITE RELIABILITY VOICE AGENT (SRVA)")
    print("=========================================")
    print("Status: ONLINE")
    print("Model:  " + model_name)
    print("-----------------------------------------")

def speak(text):
    if not text or not text.strip(): return
    print(f"\n🤖 AI: {text}")
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp_voice_final.mp3"
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
        sys.stdout.write("\r🎤 Listening...      ")
        sys.stdout.flush()
        
        # Quick adjustment
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            sys.stdout.write("\r🤔 Processing...     ")
            sys.stdout.flush()
            
            text = r.recognize_google(audio)
            print(f"\n👤 You: {text}")
            return text
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except Exception as e:
            return None

# --- 5. MAIN LOOP ---

def main():
    clear_screen()
    speak("Voice systems online. Ready for inspection.")
    
    while True:
        user_text = listen()
        
        if user_text:
            # Handle Exit
            if any(word in user_text.lower() for word in ["exit", "stop", "quit", "terminate"]):
                speak("Shutting down. Have a good evening.")
                break
            
            # Run Agent
            try:
                inputs = {"messages": [HumanMessage(content=user_text)]}
                response = agent_executor.invoke(inputs)
                
                # Parse Output
                raw_content = response["messages"][-1].content
                if isinstance(raw_content, list):
                    final_answer = raw_content[0].get("text", "")
                else:
                    final_answer = raw_content

                speak(final_answer)
                
            except Exception as e:
                print(f"\nError: {e}")
                speak("I'm having trouble connecting to the logic core.")

if __name__ == "__main__":
    main()