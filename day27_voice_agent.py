import os
import speech_recognition as sr
from gtts import gTTS
import pygame
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Pulls from .env, defaults to 2.5-flash if missing
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") 

llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# Initialize Audio
r = sr.Recognizer()
pygame.mixer.init()

def speak(text):
    """The Voice Output"""
    print(f"🤖 AI: {text}")
    tts = gTTS(text=text, lang='en')
    filename = "temp_voice.mp3"
    try:
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        pygame.mixer.music.unload()
    except Exception as e:
        print(f"Audio Error: {e}")

def listen():
    """The Voice Input"""
    with sr.Microphone() as source:
        print("\n🎤 Listening... (Speak now)")
        # Adjust for ambient noise (e.g., porch wind)
        r.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = r.listen(source, timeout=5)
            print("Processing audio...")
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return None
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return None
        except Exception as e:
            print(f"Error: {e}")
            return None

def main():
    # The Persona
    system_prompt = """
    You are 'OpsBot', a helpful Site Reliability Engineer assistant. 
    Keep your answers brief, professional, and conversational (1-2 sentences).
    Do not use markdown formatting (like bold/asterisks) as this will be spoken aloud.
    """
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    chain = prompt | llm

    speak("Voice Interface Online. Ready for commands.")
    
    while True:
        user_text = listen()
        
        if user_text:
            if "exit" in user_text.lower() or "stop" in user_text.lower():
                speak("Shutting down voice interface.")
                break
                
            # Generate AI Response
            response = chain.invoke({"input": user_text})
            speak(response.content)

if __name__ == "__main__":
    main()