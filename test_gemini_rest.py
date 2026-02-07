import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-001:predict?key={api_key}"
headers = {"Content-Type": "application/json"}
data = {
    "instances": [
        {"prompt": "A simple flat design educational illustration of a cat."}
    ],
    "parameters": {
        "sampleCount": 1
    }
}

print(f"POST {url.split('?')[0]}...")

try:
    response = requests.post(url, headers=headers, json=data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("Success! Response contains data.")
        # print first 100 chars of response to confirm structure
        print(response.text[:200])
    else:
        print("Error response:")
        print(response.text)
except Exception as e:
    print(f"Exception: {e}")
