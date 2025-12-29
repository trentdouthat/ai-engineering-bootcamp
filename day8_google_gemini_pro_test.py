import os
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file
google_api_key = os.getenv("GOOGLE_API_KEY")

from langchain_google_genai import GoogleGenerativeAI
llm = GoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=google_api_key, temperature=0)
print(llm.invoke("What are some of the pros and cons of Python as a programming language?"))
           