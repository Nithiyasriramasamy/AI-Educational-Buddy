import os
import torch
from diffusers import StableDiffusionPipeline, DiffusionPipeline
from PIL import Image

# Global pipeline cache to avoid reloading model on every request
pipe = None

def get_pipeline():
    global pipe
    if pipe is not None:
        return pipe
        
    print("Loading Stable Diffusion model...")
    # Using a lightweight model or standard 1.5 depending on resource availability
    # fast-dream-shaper-v1-5-turbo is good for speed/quality balance
    model_id = "runwayml/stable-diffusion-v1-5" 
    
    auth_token = os.environ.get("HF_TOKEN")
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")
    
    try:
        if device == "cuda":
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, 
                torch_dtype=torch.float16, 
                use_auth_token=auth_token
            )
            pipe = pipe.to("cuda")
        else:
            # CPU optimization
            pipe = StableDiffusionPipeline.from_pretrained(
                model_id, 
                use_auth_token=auth_token
            )
            pipe = pipe.to("cpu")
            # Enable attention slicing for lower memory usage on CPU
            pipe.enable_attention_slicing()
            
    except Exception as e:
        print(f"Error loading model: {e}")
        # Fallback or re-raise
        raise e
        
    return pipe

def generate_scene_image(prompt, scene_num, output_dir):
    """
    Generates an image for a specific scene and saves it.
    """
    try:
        pipeline = get_pipeline()
        
        # Enhanced negative prompt for educational style
        negative_prompt = "text, writing, watermark, signature, ugly, distorted, realistic photo, cinematic, dramatic lighting, fantasy, complex, cluttered, blurry, bad anatomy"
        
        print(f"Generating image for Scene {scene_num}...")
        image = pipeline(
            prompt=prompt, 
            negative_prompt=negative_prompt,
            num_inference_steps=25 if torch.cuda.is_available() else 15, # Fewer steps on CPU
            guidance_scale=7.5
        ).images[0]
        
        filename = f"scene_{scene_num}.png"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)
        print(f"Saved: {filepath}")
        return filename
        
    except Exception as e:
        print(f"Failed to generate image for scene {scene_num}: {e}")
        return None
