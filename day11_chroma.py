import os
from dotenv import load_dotenv
import shutil
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. Setup Brain & Embeddings
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.5-flash-lite")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

# 2. Prepare the Persistent DB
# If the folder exists, we delete it to start fresh for this test.
# In production, you would NOT delete this!
if os.path.exists("./chroma_db"):
    shutil.rmtree("./chroma_db")

# 3. Create the Database on Disk
print("--- CREATING DATABASE ---")
db = Chroma(
    collection_name="project_skyline",
    embedding_function=embeddings,
    persist_directory="./chroma_db"  # <--- This saves it to your hard drive!
)

# 4. Add Data (Only do this once!)
print("--- ADDING DOCUMENTS ---")
docs = [
    Document(page_content="Project Skyline is a migration of legacy servers to Kansas City."),
    Document(page_content="The budget for Skyline is $5 million."),
    Document(page_content="The project lead is Sarah Connor."),
    Document(page_content="Phase 1 must be completed by Q4 2025.")
]
db.add_documents(docs)
print("Documents saved to ./chroma_db folder.")

# 5. Retrieve from Disk
# Now we create a retriever that looks at that folder
retriever = db.as_retriever()

# 6. Run the Chain
template = """Answer strictly based on the context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

print("\n--- QUERYING DATABASE ---")
response = chain.invoke("When must Phase 1 be done?")
print(f"Answer: {response.content}")