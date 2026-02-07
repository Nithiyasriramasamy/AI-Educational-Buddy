import os
import json
import re
from groq import Groq

def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    return Groq(api_key=api_key)

def generate_scene_prompts(script):
    """
    Splits the script into scenes and generates detailed image prompts for each scene.
    Returns a list of dictionaries with keys: 
    scene_number, concept, diagram_type, visual_elements, relationships, image_prompt.
    """
    client = get_client()
    
    system_prompt = """You are an expert visual director for educational videos. 
    Analyze the provided teaching script and split it into logical scenes.
    
    GOAL:
    Generate high-quality, detailed, teaching-slide style image prompts for each scene.
    
    REQUIREMENTS:
    1. Each scene prompt must include:
       - concept: Short title of the concept (2-5 words)
       - diagram_type: One of (flowchart / comparison / process / timeline / labeled diagram / illustration)
       - visual_elements: List of specific objects, icons, or symbols to show.
       - relationships: List of relationships, arrows, or flow steps between elements.
       - image_prompt: A very detailed text prompt for image generation.
    
    PROMPT RULES for 'image_prompt':
    - Educational slide illustration
    - Simple flat vector design
    - White background
    - Clear diagram layout
    - Use arrows, boxes, icons
    - Only short labels (1-3 words max) if text is needed (but prefer no text)
    - No paragraphs of text
    - Student-friendly, high clarity
    - Avoid cinematic, realistic, artistic, fantasy styles
    
    OUTPUT FORMAT:
    Return ONLY a valid JSON array of objects. Do not include markdown formatting, code blocks, or explanations.
    
    Format example:
    [
      {
        "scene_number": 1,
        "concept": "Water Evaporation",
        "diagram_type": "process",
        "visual_elements": ["Sun icon", "Ocean waves", "Rising steam arrows"],
        "relationships": ["Sun heats water", "Water turns to vapor"],
        "image_prompt": "A simple flat vector educational illustration of water evaporation. White background. On the left, a bright yellow sun icon with rays pointing down. Below, blue stylized ocean waves. Upward pointing wavy arrows representing steam rising from the water. Clear, minimal design."
      }
    ]
    """
    
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Script to visualize:\n\n{script}"}
            ],
            model="llama-3.3-70b-versatile",
            temperature=0.2, # Low temperature for consistent JSON
            max_tokens=2048
        )
        
        content = response.choices[0].message.content
        
        # Clean up potential markdown code blocks if the model adds them
        content = CleanJsonMarkdown(content)
        
        # Parse JSON
        scenes = json.loads(content)
        return scenes

    except Exception as e:
        print(f"Error generating prompts: {e}")
        # Return a fallback or re-raise
        raise e

def CleanJsonMarkdown(json_content):
    """
    Removes markdown code fencing (```json ... ```) if present.
    """
    pattern = r"```json\s*(.*?)\s*```"
    match = re.search(pattern, json_content, re.DOTALL)
    if match:
        return match.group(1)
    
    # Also check for just ``` ... ```
    pattern_generic = r"```\s*(.*?)\s*```"
    match_generic = re.search(pattern_generic, json_content, re.DOTALL)
    if match_generic:
        return match_generic.group(1)
        
    return json_content.strip()

if __name__ == "__main__":
    # Test block to run directly
    from dotenv import load_dotenv
    load_dotenv()
    
    test_script = "Photosynthesis is the process by which green plants create food. Sunlight acts as the energy source. Water is absorbed by roots, and Carbon Dioxide enters through leaves. They combine to make Sugar and Oxygen."
    print("Generating prompts for test script...")
    try:
        result = generate_scene_prompts(test_script)
        print(json.dumps(result, indent=2))
    except Exception as e:
        print(f"Failed: {e}")
