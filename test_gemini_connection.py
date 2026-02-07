import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key present: {bool(api_key)}")

try:
    genai.configure(api_key=api_key)
    print("Configuration successful.")
    
    # List available models to check if we can see image generation models
    print("\nListing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
             print(f"- {m.name}")
        if 'image' in m.name.lower():
             print(f"Found visual model: {m.name}")

    print("\nAttempting to instantiate ImageGenerationModel...")
    try:
        # Try the one we used
        model_name = "imagen-3.0-generate-001"
        print(f"Testing model: {model_name}")
        model = genai.ImageGenerationModel(model_name)
        response = model.generate_images(
            prompt="A simple drawing of a cat",
            number_of_images=1
        )
        print("Success! Image generated.")
    except Exception as e:
        print(f"Error with {model_name}: {e}")
        
except Exception as e:
    print(f"General error: {e}")
