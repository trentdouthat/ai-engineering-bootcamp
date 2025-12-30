import streamlit as st
import os
import tempfile
import base64
import mimetypes
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage

# 1. Config & Setup
st.set_page_config(page_title="OpsVision Scanner", layout="wide")
load_dotenv()

# Load API Key safely
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("API Key not found. Check .env")
    st.stop()

# Initialize AI
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)

# Initialize DB (Read-Only)
DB_PATH = "./chroma_db_opsvision"
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
# Check if DB exists
if os.path.exists(DB_PATH):
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
else:
    st.error("Database not found! Please run day21_ingest.py first.")
    st.stop()

# --- HELPER FUNCTIONS ---

def encode_image(image_file):
    """Convert uploaded file to base64 for Gemini"""
    bytes_data = image_file.getvalue()
    mime_type = image_file.type
    base64_data = base64.b64encode(bytes_data).decode('utf-8')
    return mime_type, base64_data

def identify_equipment(mime, data):
    """Ask Vision Model what is in the picture"""
    prompt = """
    Analyze this technical image. Identify the top 3 distinct pieces of equipment or infrastructure.
    Return ONLY a comma-separated list. (Example: Server, Switch, Cables)
    """
    msg = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}}
    ])
    response = llm.invoke([msg])
    return response.content.strip()

# --- THE UI ---

st.title("👁️ OpsVision: Inventory Scanner")
st.caption("Upload a photo of a server rack or circuit board to retrieve specs.")

with st.sidebar:
    st.header("Upload Image")
    uploaded_file = st.file_uploader("Choose an image...", type=['png', 'jpg', 'jpeg'])

if uploaded_file:
    # Layout: 2 Columns
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    
    with col2:
        if st.button("Analyze Equipment", type="primary"):
            with st.spinner("Scanning image..."):
                # 1. Vision Phase
                mime, data = encode_image(uploaded_file)
                detected_text = identify_equipment(mime, data)
                
                st.success("Analysis Complete")
                st.subheader(f"Detected: {detected_text}")
                
                # 2. Retrieval Phase
                items = [item.strip() for item in detected_text.split(',')]
                
                st.divider()
                st.markdown("### 📄 Technical Documentation Found")
                
                for item in items:
                    with st.expander(f"Specs for: {item}", expanded=True):
                        # Search DB
                        results = db.similarity_search(item, k=1)
                        if results:
                            # Display the content found in the manual
                            st.markdown(f"**Source:** Internal Manuals")
                            st.info(results[0].page_content)
                        else:
                            st.warning("No specific manual found in database.")
else:
    st.info("Please upload an image to begin.")