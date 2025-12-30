import os
import base64
import mimetypes
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from gtts import gTTS
import pygame
import time

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# Define paths
audio_query_path = "data/Recording.m4a"
image_path = "data/server_rack.png"
audio_response_path = "data/response.mp3"

# --- HELPER FUNCTIONS ---

# 2. UPDATED Helper Function
def encode_media(path):
    """Encodes image or audio to base64 and handles Windows .m4a files"""
    
    # Force the correct MIME type for Windows Voice Recorder files
    if path.lower().endswith(".m4a"):
        mime_type = "audio/mp4"
    else:
        # Let Python guess for everything else (jpg, png, mp3, wav)
        mime_type, _ = mimetypes.guess_type(path)
    
    # Fallback if guessing fails
    if not mime_type:
        mime_type = "audio/mp3" 
    
    with open(path, "rb") as file:
        data = base64.b64encode(file.read()).decode('utf-8')
        
    return mime_type, data

def speak_text(text):
    """Converts text to speech and plays it"""
    print(f"\n--- SPEAKING: {text[:50]}... ---")
    
    # Generate MP3
    tts = gTTS(text=text, lang='en')
    tts.save(audio_response_path)
    
    # Play MP3
    pygame.mixer.init()
    pygame.mixer.music.load(audio_response_path)
    pygame.mixer.music.play()
    
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    # Cleanup (Optional: releases file lock)
    pygame.mixer.quit()

# --- MAIN EXECUTION ---

try:
    print("--- 1. LISTENING TO YOUR QUESTION ---")
    mime_audio, audio_data = encode_media(audio_query_path)
    
    print("--- 2. LOOKING AT THE IMAGE ---")
    mime_image, image_data = encode_media(image_path)

    # We send BOTH the audio question and the image to the AI at once
    # Gemini is smart enough to know the audio is referring to the image
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Listen to this audio question and answer it based on the image provided."},
            {"type": "image_url", "image_url": {"url": f"data:{mime_audio};base64,{audio_data}"}},
            {"type": "image_url", "image_url": {"url": f"data:{mime_image};base64,{image_data}"}}
        ]
    )

    print("--- 3. THINKING... ---")
    response = llm.invoke([message])
    ai_text = response.content
    
    print(f"AI Response: {ai_text}")
    
    # Step 4: Speak the answer
    speak_text(ai_text)

except FileNotFoundError as e:
    print(f"Error: Missing file! {e}")
except Exception as e:
    print(f"Error: {e}")