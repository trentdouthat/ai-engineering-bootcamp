import shutil
import tempfile
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

# 1. Setup Brain
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(google_api_key=api_key, model="gemini-2.5-flash")
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004", google_api_key=api_key)

# 2. Reset DB by creating a temporary database directory that Windows manages for us
persist_dir = tempfile.mkdtemp()

# 3. Create Data with METADATA
# This is the "Enterprise" skill. Data isn't just text; it has tags.
docs = [
    Document(
        page_content="Employees can work remotely on Fridays.", 
        metadata={"department": "IT", "year": 2025}
    ),
    Document(
        page_content="Remote work is strictly prohibited.", 
        metadata={"department": "Manufacturing", "year": 2025}
    ),
    Document(
        page_content="Bonus payouts are 10% of salary.", 
        metadata={"department": "Sales", "year": 2024}
    )
]

print("--- INDEXING POLICIES WITH METADATA ---")
db = Chroma.from_documents(
    docs, 
    embeddings, 
    persist_directory=persist_dir
)

# 4. The "Hybrid" Retriever
# We want to ask about "Remote Work", but ONLY for the "IT" department.
# If we didn't filter, the AI might see the "Strictly prohibited" rule from Manufacturing!
retriever = db.as_retriever(
    search_kwargs={
        "k": 2, # Get top 2 results
        "filter": {"department": "IT"} # <--- THE CRITICAL FILTER
    }
)

# 5. The Chain
template = """Answer based on the context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# 6. Run It
print("\n--- ASKING: 'Can I work from home?' (Filter: IT) ---")
response = chain.invoke("Can I work from home?")
print(f"AI Answer: {response.content}")

# 7. Prove the Negative
# Let's try searching the SAME question but filtering for "Manufacturing"
print("\n--- ASKING: 'Can I work from home?' (Filter: Manufacturing) ---")
manu_retriever = db.as_retriever(
    search_kwargs={"filter": {"department": "Manufacturing"}}
)
manu_chain = (
    {"context": manu_retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)
response_manu = manu_chain.invoke("Can I work from home?")
print(f"AI Answer: {response_manu.content}")