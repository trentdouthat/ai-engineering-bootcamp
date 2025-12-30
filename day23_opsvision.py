import streamlit as st
import pandas as pd
import time
import base64
from datetime import datetime
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.messages import HumanMessage

# 1. Config & Setup
st.set_page_config(page_title="OpsVision Pro", page_icon="👁️", layout="wide")
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

# Initialize AI & DB
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model=model_name)
DB_PATH = "./chroma_db_opsvision"
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# Safe DB Loading
if os.path.exists(DB_PATH):
    db = Chroma(persist_directory=DB_PATH, embedding_function=embeddings)
else:
    st.error("Database missing. Run day21_ingest.py!")
    st.stop()

# --- HELPER FUNCTIONS ---

def get_base64(file):
    return base64.b64encode(file.getvalue()).decode('utf-8')

def analyze_image(file):
    mime_type = file.type
    base64_data = get_base64(file)
    
    prompt = """
    Analyze this technical image. Return a comma-separated list of the 
    top 3 distinct technical items visible. (e.g. Raspberry Pi, Ethernet Port, GPIO Pins)
    """
    
    msg = HumanMessage(content=[
        {"type": "text", "text": prompt},
        {"type": "image_url", "image_url": {"url": f"data:{mime_type};base64,{base64_data}"}}
    ])
    
    response = llm.invoke([msg])
    return response.content.strip()

# --- UI LAYOUT ---

st.title("👁️ OpsVision Pro")
st.markdown("### Intelligent Inventory & Spec Retrieval")

with st.sidebar:
    st.header("Upload")
    uploaded_file = st.file_uploader("Drop image here", type=['png', 'jpg', 'jpeg'])
    st.divider()
    st.info("Supported: Server Racks, Circuit Boards, Cabling")

# Initialize Session State to hold data
if 'inventory_data' not in st.session_state:
    st.session_state['inventory_data'] = []

if uploaded_file:
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.image(uploaded_file, caption="Target Equipment", use_container_width=True)
        
        if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
            with st.spinner("Analyzing circuitry & components..."):
                # Run Vision
                detected_text = analyze_image(uploaded_file)
                items = [x.strip() for x in detected_text.split(',')]
                
                # Build Data for CSV
                new_records = []
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                for item in items:
                    # RAG Lookup
                    docs = db.similarity_search(item, k=1)
                    manual_snippet = docs[0].page_content if docs else "No manual found."
                    
                    record = {
                        "Timestamp": current_time,
                        "Item Detected": item,
                        "Manual Excerpt": manual_snippet[:100] + "..." # Truncate for CSV
                    }
                    new_records.append(record)
                
                # Update Session State
                st.session_state['inventory_data'] = new_records
                st.session_state['last_items'] = items # For display
                st.success("Scan Complete!")

    with col2:
        if 'last_items' in st.session_state:
            st.subheader("🔍 Analysis Results")
            
            # Display Cards for each item
            for i, record in enumerate(st.session_state['inventory_data']):
                with st.expander(f"Detected: {record['Item Detected']}", expanded=True):
                    st.caption(f"Scanned at: {record['Timestamp']}")
                    st.markdown(f"**Documentation Match:**")
                    st.code(record['Manual Excerpt'])

            st.divider()
            
            # CSV Download Section
            if st.session_state['inventory_data']:
                df = pd.DataFrame(st.session_state['inventory_data'])
                csv = df.to_csv(index=False).encode('utf-8')
                
                st.download_button(
                    label="📥 Download Inventory Report (CSV)",
                    data=csv,
                    file_name="opsvision_report.csv",
                    mime="text/csv",
                    type="secondary"
                )

else:
    st.info("Waiting for image...")