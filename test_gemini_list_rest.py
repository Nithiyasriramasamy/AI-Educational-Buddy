import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"

print(f"GET {url.split('?')[0]}...")

try:
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        models = response.json().get('models', [])
        print(f"Found {len(models)} models.")
        for m in models:
            # Check for image capability or name
            name = m.get('name')
            methods = m.get('supportedGenerationMethods', [])
            if 'image' in name.lower() or 'predict' in methods or 'generateContent' not in methods:
                 print(f"- {name} [{', '.join(methods)}]")
    else:
        print("Error response:")
        print(response.text)
except Exception as e:
    print(f"Exception: {e}")
