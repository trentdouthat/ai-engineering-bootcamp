import os
import time
import json
from dotenv import load_dotenv
from google import genai 
from google.genai import types

# 1. Setup (New "Client" Syntax)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") # 2.5 is perfect for this

client = genai.Client(api_key=api_key)

video_path = "data/20251230_103438.mp4" # <--- Your video file

def analyze_video_structured(path):
    print(f"--- 1. UPLOADING {path} ---")
    
    # upload_file is now cleaner in the new SDK
    video_file = client.files.upload(file=path)
    print(f"Upload Complete: {video_file.uri}")

    # 2. Wait for Processing
    print("--- 2. WAITING FOR PROCESSING ---")
    while video_file.state.name == "PROCESSING":
        print(".", end="", flush=True)
        time.sleep(2)
        video_file = client.files.get(name=video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed.")

    print(f"\nState: {video_file.state.name}")

    # 3. The Prompt with Schema (Structured Output)
    print(f"--- 3. ANALYZING WITH {model_name} ---")
    
    prompt = """
    Analyze this video. Return a JSON list of events. 
    For each event, provide:
    - start_time (string, e.g. '00:00')
    - end_time (string)
    - description (string)
    - objects_visible (list of strings)
    """

    # We instruct the model to return strictly JSON
    response = client.models.generate_content(
        model=model_name,
        contents=[video_file, prompt],
        config=types.GenerateContentConfig(
            response_mime_type="application/json" # <--- Magic Switch
        )
    )
    
    print("\n--- RAW JSON OUTPUT ---")
    # Parse the text to ensure it's valid JSON
    events = json.loads(response.text)
    print(json.dumps(events, indent=2))
    
    # 4. Cleanup (Polite to the cloud)
    # client.files.delete(name=video_file.name)

try:
    if not os.path.exists(video_path):
        print(f"Error: file {video_path} not found.")
    else:
        analyze_video_structured(video_path)

except Exception as e:
    print(f"Error: {e}")