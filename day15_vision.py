import os
import base64
import mimetypes # <--- Standard library to guess file types
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

# 1. Load Config
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
# Pull the model from .env, but default to 1.5-flash if missing
model_name = os.getenv("GEMINI_MODEL")

print(f"--- USING MODEL: {model_name} ---")

llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# 2. Image Setup
image_path = "data/server_rack.png" # <--- Update this to your actual filename!

# 3. Helper: Smart Encoding
def get_image_data(path):
    # Guess the MIME type (e.g., 'image/png' or 'image/jpeg') based on file extension
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type:
        mime_type = "image/jpeg" # Default fallback
    
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        
    return mime_type, encoded_string

try:
    # 4. Process the Image
    mime_type, image_data = get_image_data(image_path)
    print(f"Loaded image as: {mime_type}")

    # 5. The Prompt
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Analyze this technical image. Return a JSON list of the equipment or objects you see."},
            {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{image_data}"}}
        ]
    )

    print("--- SENDING TO AI ---")
    response = llm.invoke([message])
    
    print("\n--- RESULT ---")
    print(response.content)

except FileNotFoundError:
    print(f"Error: Could not find {image_path}. Check the filename.")
except Exception as e:
    print(f"Error: {e}")