import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("Listing models...")
try:
    for m in genai.list_models():
        print(f"Name: {m.name}")
        print(f"Methods: {m.supported_generation_methods}")
        print("-" * 20)
except Exception as e:
    print(f"Error listing models: {e}")
