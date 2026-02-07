import os
import requests
import base64
import time

def generate_scene_image(prompt, scene_num, output_dir):
    """
    Generate an image using NVIDIA's Stable Diffusion API.
    """
    api_key = os.environ.get("NVIDIA_API_KEY")
    if not api_key:
        print("Warning: NVIDIA_API_KEY not found")
        return None

    invoke_url = "https://ai.api.nvidia.com/v1/genai/stabilityai/stable-diffusion-xl"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }

    payload = {
        "text_prompts": [
            {
                "text": prompt,
                "weight": 1
            }
        ],
        "cfg_scale": 5,
        "sampler": "K_DPM_2_ANCESTRAL",
        "seed": 0,
        "steps": 25
    }

    try:
        print(f"Generating image with NVIDIA for scene {scene_num}...")
        response = requests.post(invoke_url, headers=headers, json=payload)
        response.raise_for_status()
        
        body = response.json()
        
        if "artifacts" in body and len(body["artifacts"]) > 0:
            artifact = body["artifacts"][0]
            image_base64 = artifact.get("base64")
            
            if image_base64:
                filename = f"scene_{scene_num}_{int(time.time())}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, "wb") as f:
                    f.write(base64.b64decode(image_base64))
                
                print(f"Saved NVIDIA image: {filepath}")
                return filename
            else:
                print("No base64 image data in response")
                return None
        else:
            print("No artifacts in NVIDIA response")
            return None

    except Exception as e:
        print(f"Error generating NVIDIA image: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")
        return None
