import os
import shutil
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

# 1. Setup
DB_PATH = "./chroma_db_opsvision"
DATA_PATH = "data/manuals"

# Clean start: Delete old DB if it exists
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)

# 2. Load Documents
print("--- LOADING MANUALS ---")
loader = DirectoryLoader(DATA_PATH, glob="*.txt", loader_cls=TextLoader)
docs = loader.load()

# 3. Split Text (Chunks)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
splits = text_splitter.split_documents(docs)

# 4. Create Vector DB
print("--- CREATING VECTOR DATABASE ---")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

db = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory=DB_PATH
)

print(f"--- SUCCESS: Ingested {len(splits)} chunks into {DB_PATH} ---")