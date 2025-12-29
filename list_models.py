import os
from dotenv import load_dotenv

import google.generativeai as genai

# Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

print("--- Checking Available Models ---")
try:
    # Ask Google for the list
    for m in genai.list_models():
        # Only show models that can generate text/chat
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
            
except Exception as e:
    print(f"Error fetching models: {e}")