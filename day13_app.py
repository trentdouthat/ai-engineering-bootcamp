import streamlit as st
import shutil
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="Day 13: Policy Bot", layout="wide")
st.title("🤖 Corporate Policy AI Assistant")

#  set the API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.warning("Please enter your API Key to start.")
    st.stop()

# --- 2. SETUP BRAIN ---
@st.cache_resource
def setup_qa_chain(api_key):
    """
    Sets up the vector DB and the LLM chain. 
    Cached so it doesn't reload on every button click.
    """
    # Initialize Models
    llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.5-flash-lite")
    embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

    # Simulated Data (The "Knowledge Base")
    docs = [
        Document(page_content="Employees can work remotely on Fridays.", metadata={"dept": "IT"}),
        Document(page_content="Remote work is strictly prohibited.", metadata={"dept": "Manufacturing"}),
        Document(page_content="The standard work hours are 9am to 5pm.", metadata={"dept": "All"}),
        Document(page_content="Overtime must be approved by a manager.", metadata={"dept": "All"}),
        Document(page_content="Vacation accrual is 1.5 days per month.", metadata={"dept": "HR"})
    ]

    # Create/Reset DB in memory (or disk)
    # For a demo app, using a temp directory is cleaner
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name="streamlit_demo"
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

    # The Prompt
    template = """Answer the question based ONLY on the context below. 
    If you don't know, say "I don't know."
    
    Context:
    {context}

    Question: {question}
    """
    prompt = ChatPromptTemplate.from_template(template)

    # The Chain
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )
    return chain

# Load the chain
try:
    chain = setup_qa_chain(api_key)
    st.success("✅ System Ready! Knowledge Base Loaded.")
except Exception as e:
    st.error(f"Error starting AI: {e}")
    st.stop()

# --- 3. THE CHAT INTERFACE ---
# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask about company policies..."):
    # 1. Show User Message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 2. Generate AI Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chain.invoke(prompt)
            st.markdown(response.content)
            
    # 3. Save History
    st.session_state.messages.append({"role": "assistant", "content": response.content})

# To configure git for committing code, use the commands below:
#   git config --global user.name "Trent Douthat"
#git config --global user.email "trent.douthat@gmail.com"