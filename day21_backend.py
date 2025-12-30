import os
import base64
import mimetypes
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage

# 1. Setup
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash") # Use your best model

llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)
DB_PATH = "./chroma_db_opsvision"
image_path = "data/server_rack.png" # <--- Ensure this exists from Day 15!

# 2. Connect to Database
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)

# 3. Helper: Encode Image
def encode_image(path):
    mime_type, _ = mimetypes.guess_type(path)
    if not mime_type: mime_type = "image/png"
    with open(path, "rb") as f:
        return mime_type, base64.b64encode(f.read()).decode('utf-8')

# --- THE PIPELINE ---

try:
    print(f"--- 1. ANALYZING IMAGE: {image_path} ---")
    mime, data = encode_image(image_path)
    
    # Step A: Ask Vision to identify items (Prompt Engineering)
    # We ask for a simple comma-separated list to make searching easier
    vision_prompt = """
    Look at this technical image. List the top 3 most distinct technical items you see.
    Format: Just the item names, separated by commas. (e.g., Server, Cable, Monitor).
    """
    
    msg = HumanMessage(content=[
        {"type": "text", "text": vision_prompt},
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}}
    ])
    
    vision_response = llm.invoke([msg])
    items_detected = vision_response.content.strip()
    print(f"DETECTED ITEMS: {items_detected}")
    
    # Step B: Loop through items and "Recall" info
    item_list = [item.strip() for item in items_detected.split(',')]
    
    print("\n--- 2. RETRIEVING SPECS FROM DATABASE ---")
    for item in item_list:
        print(f"\n>> Searching manuals for: '{item}'...")
        
        # Search the DB
        results = db.similarity_search(item, k=1)
        
        if results:
            print(f"   FOUND DOC: {results[0].page_content[:200]}...") # Print first 200 chars
        else:
            print("   No manual found.")

except Exception as e:
    print(f"Error: {e}")