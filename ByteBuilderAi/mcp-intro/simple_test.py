import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
print(f"Testing with API key: {api_key[:20]}...")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')
response = model.generate_content("Hello, world!")
print("Response:", response.text)
