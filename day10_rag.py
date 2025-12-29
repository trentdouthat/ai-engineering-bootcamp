import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. Setup Brain & Embeddings
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.5-flash-lite")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

# 2. The "Private" Data
# Imagine this is a confidential PDF you just loaded.
private_text = """
CONFIDENTIAL INTERNAL MEMO:
Project 'Skyline' is the new initiative to migrate all legacy servers to Kansas City by Q4 2025.
The budget for this project is $5 million.
The project lead is Sarah Connor.
Usage of 'Terminator' protocols is strictly prohibited.
"""

# 3. Chunking & Indexing (The "R" in RAG)
# We turn text into vectors and store them in RAM.
vector_store = InMemoryVectorStore(embeddings)
vector_store.add_documents([Document(page_content=private_text)])
retriever = vector_store.as_retriever()

# 4. The Prompt (The "A" in RAG)
template = """Answer the question based ONLY on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

# 5. The Chain (The "G" in RAG)
# This looks complex, but it just means:
# "Take question -> Find related chunk -> Stuff it into prompt -> Send to LLM"
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 6. Run it
print("--- QUESTION 1: Who is leading the project? ---")
response = chain.invoke("Who is the project lead for Skyline?")
print(response.content)

print("\n--- QUESTION 2: What is the budget? ---")
response = chain.invoke("How much money can we spend on Skyline?")
print(response.content)