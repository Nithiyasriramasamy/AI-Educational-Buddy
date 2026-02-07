import re

def clean_script_text(text):
    """
    Cleans up the script text by removing any potential markdown artifacts or unwanted whitespace.
    """
    if not text:
        return ""
    
    # Remove markdown bold/italic
    text = text.replace('**', '').replace('*', '')
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def validate_scene_data(scenes):
    """
    Validates the structure of the scene data returned by the LLM.
    Ensures each scene has the required keys.
    """
    validated_scenes = []
    for i, scene in enumerate(scenes):
        # Ensure distinct scene numbers
        scene_num = scene.get('scene_number', i + 1)
        
        # Ensure we have a prompt
        prompt = scene.get('image_prompt', 'Educational illustration with white background')
        
        # Ensure visual style keywords are present (redundancy check - though prompt generator should handle this)
        # We relax this check slightly as the new prompt generator has strict rules, 
        # but ensuring "white background" is always good for this style.
        if "white background" not in prompt.lower():
            prompt += ", white background"
            
        validated_scenes.append({
            "scene_number": scene_num,
            "concept": scene.get('concept', f"Scene {scene_num}"),
            "diagram_type": scene.get('diagram_type', "illustration"),
            "visual_elements": scene.get('visual_elements', []),
            "relationships": scene.get('relationships', []),
            "image_prompt": prompt
        })
        
    return validated_scenes
