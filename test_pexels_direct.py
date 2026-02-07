from services.pexels_image_generator import generate_scene_image
from dotenv import load_dotenv
import os
import traceback

load_dotenv()

print("Testing Pexels Integration...")
api_key = os.environ.get("PEXELS_API_KEY")
print(f"API Key present: {bool(api_key)}")

output_dir = "test_output"
os.makedirs(output_dir, exist_ok=True)

try:
    print("Attempting to search for 'Solar System'...")
    filename = generate_scene_image("A clear educational illustration of the Solar System", 1, output_dir)
    
    if filename:
        print(f"✅ Success! Image saved to: {filename}")
        full_path = os.path.join(output_dir, filename)
        if os.path.exists(full_path):
            print(f"File verified at: {full_path}")
            print(f"Size: {os.path.getsize(full_path)} bytes")
    else:
        print("❌ Failed to get image from Pexels.")

except Exception as e:
    print(f"❌ Exception occurred: {e}")
    traceback.print_exc()
