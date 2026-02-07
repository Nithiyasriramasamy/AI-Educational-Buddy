#!/usr/bin/env python3
"""
Groq API integration for enhanced script analysis and prompt generation
"""

import json
import requests
from typing import List, Dict, Any

class GroqScriptAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def analyze_script_and_generate_prompts(self, script_text: str) -> List[Dict[str, Any]]:
        """
        Use Groq API to analyze script and generate educational image prompts
        """
        try:
            system_prompt = """You are an AI assistant that converts teaching scripts into scene-wise educational image generation prompts.

TASK:
• Read the given teaching script.
• Split it into clear conceptual scenes.
• For each scene, generate ONE image prompt.
• Prompts must be educational, student-friendly, and slide-style.
• Do NOT use cinematic, artistic, fantasy, or dramatic language.
• Avoid long text inside images.
• Use clear visual explanations instead.

OUTPUT FORMAT (IMPORTANT):
Return ONLY a JSON array.
Each item must have:
- scene_number
- concept_summary  
- image_prompt

IMAGE PROMPT RULES:
• Educational illustration
• Simple flat design
• White background
• Teaching slide style
• Clear visual elements
• High clarity

Example output:
[
  {
    "scene_number": 1,
    "concept_summary": "Introduction to photosynthesis process",
    "image_prompt": "Educational illustration showing a simple plant with sunlight arrows, water droplets, and CO2 molecules, simple flat design, white background, teaching slide style, clear visual elements, high clarity"
  }
]"""

            user_prompt = f"INPUT SCRIPT:\n{script_text}"
            
            payload = {
                "model": "llama-3.1-8b-instant",  # Updated Groq model
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 2000,
                "top_p": 0.9
            }
            
            print("🤖 Analyzing script with Groq AI...")
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                content = data['choices'][0]['message']['content'].strip()
                
                # Extract JSON from response
                try:
                    # Find JSON array in the response
                    start_idx = content.find('[')
                    end_idx = content.rfind(']') + 1
                    
                    if start_idx != -1 and end_idx != 0:
                        json_str = content[start_idx:end_idx]
                        scenes = json.loads(json_str)
                        
                        print(f"✅ Groq AI generated {len(scenes)} scenes")
                        return scenes
                    else:
                        print("❌ No valid JSON found in Groq response")
                        return None
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON parsing error: {e}")
                    print(f"Raw response: {content[:200]}...")
                    return None
            else:
                print(f"❌ Groq API error: {response.status_code} - {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Groq integration error: {e}")
            return None
    
    def enhance_image_prompt(self, basic_prompt: str, concept: str) -> str:
        """
        Use Groq to enhance a basic image prompt for better educational value
        """
        try:
            system_prompt = """You are an expert at creating educational image prompts. 
            
Enhance the given prompt to be more educational and visually clear while keeping it simple and teaching-focused.

RULES:
- Keep it educational and student-friendly
- Use simple flat design style
- White background
- Clear visual elements
- No long text in images
- Teaching slide style
- High clarity

Return ONLY the enhanced prompt, nothing else."""

            user_prompt = f"Concept: {concept}\nBasic prompt: {basic_prompt}\n\nEnhance this prompt:"
            
            payload = {
                "model": "llama-3.1-8b-instant",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                "temperature": 0.2,
                "max_tokens": 200,
                "top_p": 0.8
            }
            
            response = requests.post(self.base_url, headers=self.headers, json=payload, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                enhanced_prompt = data['choices'][0]['message']['content'].strip()
                return enhanced_prompt
            else:
                print(f"❌ Prompt enhancement failed: {response.status_code}")
                return basic_prompt
                
        except Exception as e:
            print(f"❌ Prompt enhancement error: {e}")
            return basic_prompt

def test_groq_integration():
    """Test the Groq integration"""
    api_key = os.environ.get("GROQ_API_KEY")
    
    analyzer = GroqScriptAnalyzer(api_key)
    
    test_script = """First, let's understand what photosynthesis is. Photosynthesis is the process by which plants convert sunlight into energy.

Next, we'll explore the key components needed for photosynthesis. Plants need three main things: sunlight, water, and carbon dioxide.

Now, let's look at what happens during photosynthesis. The chloroplasts in plant leaves capture sunlight and use it to convert water and carbon dioxide into glucose and oxygen.

Finally, we'll discuss why photosynthesis is important. This process not only feeds the plant but also produces the oxygen we breathe."""
    
    print("🧪 Testing Groq Integration")
    print("=" * 50)
    
    scenes = analyzer.analyze_script_and_generate_prompts(test_script)
    
    if scenes:
        print(f"\n✅ Generated {len(scenes)} scenes:")
        for scene in scenes:
            print(f"\nScene {scene['scene_number']}:")
            print(f"  Concept: {scene['concept_summary']}")
            print(f"  Prompt: {scene['image_prompt'][:100]}...")
        return True
    else:
        print("❌ Groq integration test failed")
        return False

if __name__ == "__main__":
    test_groq_integration()