import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Pull model from .env!
model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash") 

genai.configure(api_key=api_key)

video_path = "data/20251230_103438.mp4" 

def analyze_video(path):
    print(f"--- 1. UPLOADING {path} ---")
    video_file = genai.upload_file(path=path)
    print(f"Upload Complete: {video_file.uri}")

    # 2. Wait for Processing
    print("--- 2. WAITING FOR PROCESSING ---")
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed.")

    print(f"\nState: {video_file.state.name}")

    # 3. The Prompt
    print(f"--- 3. ANALYZING WITH {model_name} ---")
    
    # Use the variable from .env
    model = genai.GenerativeModel(model_name=model_name)
    
    prompt = "Watch this video carefully. Describe exactly what happens, and provide a timeline of events."
    
    response = model.generate_content([video_file, prompt])
    
    print("\n--- VIDEO ANALYSIS ---")
    print(response.text)

try:
    if not os.path.exists(video_path):
        print(f"Error: file {video_path} not found.")
    else:
        analyze_video(video_path)

except Exception as e:
    print(f"Error: {e}")