import os
import requests
import re
from urllib.parse import urlparse

def generate_scene_image(prompt, scene_num, output_dir):
    """
    Search Pexels for an image matching the prompt and save it.
    """
    api_key = os.environ.get("PEXELS_API_KEY")
    if not api_key:
        print("Warning: PEXELS_API_KEY not found")
        return None
        
    try:
        # Simplify prompt for Pexels search
        # Remove style instructions to focus on the subject
        remove_phrases = [
            "simple flat design", "flat design", "educational illustration", 
            "white background", "teaching slide style", "student friendly",
            "clear visual elements", "no long text", "high clarity",
            "illustration explaining", "Explaining", "Visualization of"
        ]
        
        search_query = prompt
        for phrase in remove_phrases:
            search_query = search_query.replace(phrase, "")
            search_query = search_query.replace(phrase.lower(), "")
            
        # Clean up commas and extra spaces
        search_query = re.sub(r'[,.]', '', search_query)
        search_query = re.sub(r'\s+', ' ', search_query).strip()
        
        # Fallback if query becomes empty
        if len(search_query) < 3:
            search_query = "education"
            
        print(f"Searching Pexels for: '{search_query}' (Original: {prompt[:30]}...)")
        
        headers = {"Authorization": api_key}
        url = f"https://api.pexels.com/v1/search?query={search_query}&per_page=1&orientation=landscape"
        
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data['photos']:
                photo = data['photos'][0]
                image_url = photo['src']['large'] # Good quality for video
                
                print(f"Found image: {image_url}")
                
                # Download image
                img_data = requests.get(image_url).content
                
                filename = f"scene_{scene_num}.jpg"
                filepath = os.path.join(output_dir, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                    
                print(f"Saved: {filepath}")
                return filename
            else:
                print(f"No results found on Pexels for: {search_query}")
                return None
        else:
            print(f"Pexels API Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"Error fetching Pexels image: {e}")
        return None
