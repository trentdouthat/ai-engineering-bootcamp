import os
import numpy as np
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv

# 1. Setup - Use the key you already created
load_dotenv()  # Load environment variables from .env file
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("API Key not found! Check your .env file.")
os.environ["GOOGLE_API_KEY"] = api_key

# 2. Initialize the Embedding Model
# We use a specific model optimized for turning text into vectors
embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")

# 3. The Data: A list of sentences
documents = [
    "The dog chased the ball.",
    "The cat sleeps on the sofa.",
    "I love coding in Python.",
    "Machine learning is fascinating."
]

print("--- 1. Generating Embeddings ---")
# Turn the documents into numbers (vectors)
doc_vectors = embeddings.embed_documents(documents)
print(f"Generated {len(doc_vectors)} vectors.")
print(f"Vector length (dimensions): {len(doc_vectors[0])} numbers per sentence.")

# 4. The Query
query = "Feline animal"
print(f"\n--- 2. Comparing Query: '{query}' ---")
query_vector = embeddings.embed_query(query)

# 5. The Math (Cosine Similarity)
# This calculates how close the "angles" of the vectors are.
# 1.0 = Identical meaning, 0.0 = Unrelated
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

for i, doc_vec in enumerate(doc_vectors):
    score = cosine_similarity(query_vector, doc_vec)
    print(f"Score: {score:.4f} | Sentence: {documents[i]}")