import os
import mimetypes
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
import base64

# 1. Load Config
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL")

llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# 2. Audio Setup
audio_path = "data/voice3.mp3" # <--- Update this to your filename!

# 3. Helper: Encode Audio
def get_audio_data(path):
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "audio/mp3" # Fallback
    
    with open(path, "rb") as audio_file:
        encoded_string = base64.b64encode(audio_file.read()).decode('utf-8')
        
    return mime_type, encoded_string

try:
    # 4. Process Audio
    print(f"--- LISTENING TO {audio_path} ---")
    mime_type, audio_data = get_audio_data(audio_path)

    # 5. The Prompt
    # We ask for TWO things: Transcription AND Action Items.
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Please transcribe this audio exactly. Then, extract any action items or technical issues mentioned."},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{audio_data}"}}
        ]
    )
    # Note: LangChain uses "image_url" for all media types (audio/video/image) right now. 
    # It's a quirk of the library, but it works!

    response = llm.invoke([message])
    
    print("\n--- AI AUDIO ANALYSIS ---")
    print(response.content)

except FileNotFoundError:
    print(f"Error: Could not find {audio_path}. Did you record a file?")
except Exception as e:
    print(f"Error: {e}")