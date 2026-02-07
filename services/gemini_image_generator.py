import os
import google.generativeai as genai
from PIL import Image
import io

# Configure the library
def configure_gemini():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Warning: GEMINI_API_KEY not found in environment variables")
        return False
    genai.configure(api_key=api_key)
    return True

def generate_scene_image(prompt, scene_num, output_dir):
    """
    Generates an image using Gemini Image Generation model and saves it.
    """
    if not configure_gemini():
        return None

    try:
        # Enforce educational style constraints
        style_guide = (
            "Create a simple, flat design educational illustration with a white background. "
            "The image should be student-friendly with clear visual elements and high clarity. "
            "Avoid text inside the image. Avoid cinematic, dramatic, or artistic styles. "
        )
        full_prompt = f"{style_guide} Visualization: {prompt}"
        
        print(f"Generating image for Scene {scene_num} with Gemini...")
        
        # Using the standard image generation model
        # Note: The model name might vary, 'imagen-3.0-generate-001' is a common target 
        # but 'gemini-1.5-flash' or similar vision models generate text-from-image.
        # For Image Generation specifically, we use the specific Imagen model if available 
        # via this SDK, or the 'models/imagen-3.0-generate-001' endpoint.
        
        # As of early 2025/late 2024, the python SDK supports image generation via:
        model = genai.ImageGenerationModel("imagen-3.0-generate-001")
        
        response = model.generate_images(
            prompt=full_prompt,
            number_of_images=1,
        )
        
        if response and response.images:
            image = response.images[0]
            
            # Create filename
            filename = f"scene_{scene_num}.png"
            filepath = os.path.join(output_dir, filename)
            
            # Save the image
            image.save(filepath)
            print(f"Saved: {filepath}")
            return filename
        else:
            print(f"No image returned for scene {scene_num}")
            return None
            
    except Exception as e:
        print(f"Failed to generate image for scene {scene_num} via Gemini: {e}")
        # Fallback logic could go here, but for MVP we return None
        return None
