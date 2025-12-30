import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load env immediately when imported
load_dotenv()

class VideoIntelligence:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
        
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env")
            
        self.client = genai.Client(api_key=self.api_key)

    def upload_video(self, file_path):
        """Uploads a local video file to Gemini"""
        print(f"Uploading {file_path}...")
        video_file = self.client.files.upload(file=file_path)
        return video_file

    def wait_for_processing(self, video_file):
        """Polls the API until the video is ready"""
        print("Waiting for video processing...")
        while video_file.state.name == "PROCESSING":
            time.sleep(2)
            video_file = self.client.files.get(name=video_file.name)
        
        if video_file.state.name == "FAILED":
            raise ValueError("Video processing failed.")
            
        return video_file

    def query_video(self, video_file, user_question):
        """Sends a question about the video to the AI"""
        prompt = f"""
        Answer this question based on the video provided: "{user_question}"
        Provide a detailed answer and timestamp if applicable.
        """
        
        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[video_file, prompt]
        )
        return response.text

    def get_video_timeline(self, video_file):
        """Asks Gemini for a structured JSON timeline of events"""
        from google.genai import types # Import inside function or at top
        import json

        prompt = """
        Analyze this video. Return a JSON list of events. 
        For each event, provide:
        - start (string, e.g. '00:00')
        - end (string)
        - event_description (string)
        """

        response = self.client.models.generate_content(
            model=self.model_name,
            contents=[video_file, prompt],
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        
        # Return Python List (parsed from JSON)
        return json.loads(response.text)

# --- TEST BLOCK ---
# This only runs if you execute this file directly (not when imported)
if __name__ == "__main__":
    try:
        # Initialize
        ai = VideoIntelligence()
        
        # Test with your existing video
        video_path = "data/20251230_103438.mp4" 
        
        if os.path.exists(video_path):
            # 1. Upload
            vf = ai.upload_video(video_path)
            
            # 2. Wait
            vf = ai.wait_for_processing(vf)
            
            # 3. Ask
            print("\n--- ASKING QUESTION ---")
            answer = ai.query_video(vf, "Describe the desk setup in detail.")
            print(answer)
            
            # Cleanup (Optional)
            # ai.client.files.delete(name=vf.name)
        else:
            print("Video file not found for testing.")
            
    except Exception as e:
        print(f"Error: {e}")