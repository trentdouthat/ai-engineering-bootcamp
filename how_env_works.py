import os
from dotenv import load_dotenv

# 1. "Put on the reading glasses" (Read the .env file)
load_dotenv() 

# 2. "Ask the System for the key"
# If the .env file wasn't there, this would return None (blank).
my_secret = os.getenv("GOOGLE_API_KEY")
print(f"My Google API Key is: {my_secret}")