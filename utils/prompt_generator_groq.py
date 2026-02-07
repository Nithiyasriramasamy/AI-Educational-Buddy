import os
import json
from groq import Groq

# Initialize Groq client
# Note: Client will look for GROQ_API_KEY in environment variables
def get_client():
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")
    return Groq(api_key=api_key)

def generate_script_from_topic(topic, profile=None):
    """
    Generates a teaching script based on the provided topic and student profile.
    """
    client = get_client()

    # Default profile if none provided
    if not profile:
        profile = {
            "knowledge_level": "beginner",
            "english_level": "normal",
            "examples_needed": "yes",
            "confidence_level": "medium",
            "learning_speed": "normal"
        }
    
    system_prompt = f"""You are an adaptive AI teacher.

    TASK:
    Generate a teaching script for the given topic.
    The script must be written based on the student's learning values.

    STUDENT PROFILE:
    - Knowledge level: {profile.get('knowledge_level', 'beginner')}
    - English level: {profile.get('english_level', 'normal')}
    - Needs real-life examples: {profile.get('examples_needed', 'yes')}
    - Learning speed: {profile.get('learning_speed', 'normal')}
    - Confidence level: {profile.get('confidence_level', 'medium')}

    SCRIPT RULES:
    - Adjust explanation depth based on knowledge level
    - Use very simple English if specified
    - Add real-life examples if required
    - Use step-by-step explanation for slow learners
    - Keep it encouraging if confidence is low
    - Avoid unnecessary technical terms
    - Suitable for a 1–2 minute teaching video
    - Divide naturally into 5–7 short scenes

    OUTPUT FORMAT:
    Return ONLY plain text script.
    Separate each scene using: [SCENE]
    Do not number the scenes yourself, just use the separator.
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"TOPIC: {topic}"}
        ],
        model="llama-3.3-70b-versatile",
    )
    
    return response.choices[0].message.content

def generate_scene_prompts(script):
    """
    Splits the script into scenes and generates image prompts for each scene.
    Returns a list of dictionaries with keys: scene_number, concept_summary, image_prompt.
    """
    client = get_client()
    
    system_prompt = """You are an expert visual director for educational videos. 
    Analyze the provided teaching script and split it into logical scenes.
    For each scene, provide:
    1. A brief concept summary.
    2. A specific image prompt for Stable Diffusion.
    
    VISUAL STYLE RULES:
    - Simple flat educational illustration
    - White background
    - Student friendly
    - Clear visual elements
    - NO cinematic, artistic, dramatic, fantasy words
    - NO text inside images (or very minimal)
    
    OUTPUT FORMAT:
    Return ONLY a valid JSON array of objects. Do not include markdown formatting or explanations.
    Format:
    [
      {"scene_number": 1, "concept_summary": "...", "image_prompt": "..."},
      ...
    ]
    """
    
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Script to visualize:\n\n{script}"}
        ],
        model="llama-3.3-70b-versatile",
        temperature=0.3 # Lower temperature for more consistent JSON
    )
    
    content = response.choices[0].message.content
    
    # Simple cleanup to ensure we get just the JSON part if the model chats a bit
    try:
        # Find the first '[' and last ']'
        start_idx = content.find('[')
        end_idx = content.rfind(']') + 1
        if start_idx != -1 and end_idx != -1:
            json_str = content[start_idx:end_idx]
            return json.loads(json_str)
        else:
            raise ValueError("No JSON array found in response")
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {content}")
        raise e
