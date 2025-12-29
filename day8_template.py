import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

# 1. Setup the Brain
# (We use the key directly here to keep it simple for now)
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
llm = ChatGoogleGenerativeAI(
    google_api_key=api_key, 
    model="gemini-flash-latest"
)

# 2. The "Form" (Prompt Template)
# Think of {topic} as a blank space in a form.
template = PromptTemplate(
    input_variables=["topic"],
    template="Explain the technical concept '{topic}' to a non-technical recruiter in 2 sentences."
)

# 3. The Chain
# This connects the Form -> to the Brain
chain = template | llm

# 4. Run it
# This is the Python Dictionary part:
# We are saying: "Set 'topic' equal to 'Docker'"
input_data = {"topic": "Docker Containers"}

response = chain.invoke(input_data)

print(f"--- Explaining: {input_data['topic']} ---")
print(response.content)