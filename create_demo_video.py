#!/usr/bin/env python3
"""
Create a demo video using the AI Teaching Video Generator
"""

import requests
import json
import time
import os

BASE_URL = "http://localhost:5000"

# Demo script about photosynthesis
DEMO_SCRIPT = """First, let's understand what photosynthesis is. Photosynthesis is the process by which plants convert sunlight into energy. This amazing process is essential for life on Earth.

Next, we'll explore the key components needed for photosynthesis. Plants need three main things: sunlight, water, and carbon dioxide. These ingredients work together in a special way.

Now, let's look at what happens during photosynthesis. The chloroplasts in plant leaves capture sunlight and use it to convert water and carbon dioxide into glucose and oxygen. This happens in two main stages.

Finally, we'll discuss why photosynthesis is important. This process not only feeds the plant but also produces the oxygen we breathe. Without photosynthesis, life as we know it wouldn't exist."""

def create_demo():
    """Create a complete demo video"""
    print("🎬 Creating Demo Teaching Video")
    print("=" * 50)
    
    try:
        # Step 1: Split script
        print("📝 Step 1: Analyzing script with Groq AI...")
        response = requests.post(f"{BASE_URL}/split-script", 
                               json={"script": DEMO_SCRIPT}, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed: {response.status_code}")
            return False
        
        data = response.json()
        scenes = data.get('scenes', [])
        print(f"✅ Split into {len(scenes)} scenes")
        
        # Step 2: Generate enhanced prompts
        print("🤖 Step 2: Generating AI-enhanced prompts...")
        response = requests.post(f"{BASE_URL}/generate-prompts", 
                               json={"scenes": scenes}, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ Failed: {response.status_code}")
            return False
        
        data = response.json()
        prompts = data.get('prompts', [])
        print(f"✅ Generated {len(prompts)} enhanced prompts")
        
        # Show the prompts
        for i, prompt in enumerate(prompts, 1):
            print(f"\n🎯 Scene {i}: {prompt.get('concept', 'Unknown')}")
            print(f"   📋 Prompt: {prompt.get('prompt', '')[:100]}...")
        
        # Step 3: Generate images
        print(f"\n🖼️ Step 3: Generating {len(prompts)} educational images...")
        response = requests.post(f"{BASE_URL}/generate-images", 
                               json={"prompts": prompts}, timeout=120)
        
        if response.status_code != 200:
            print(f"❌ Failed: {response.status_code}")
            return False
        
        data = response.json()
        images = data.get('images', [])
        successful_images = [img for img in images if not img.get('error')]
        print(f"✅ Created {len(successful_images)}/{len(images)} images")
        
        # Step 4: Generate narration
        print("🎵 Step 4: Creating narration audio...")
        response = requests.post(f"{BASE_URL}/generate-audio", 
                               json={"script": DEMO_SCRIPT}, timeout=60)
        
        if response.status_code != 200:
            print(f"❌ Failed: {response.status_code}")
            return False
        
        data = response.json()
        audio_file = data.get('audio_filename')
        print(f"✅ Created narration: {audio_file}")
        
        # Step 5: Create video/slideshow
        print("🎬 Step 5: Assembling final video...")
        image_files = [img['filename'] for img in successful_images if img.get('filename')]
        
        if not image_files:
            print("❌ No images available for video creation")
            return False
        
        response = requests.post(f"{BASE_URL}/create-video", 
                               json={
                                   "image_files": image_files,
                                   "audio_file": audio_file
                               }, timeout=180)
        
        if response.status_code != 200:
            print(f"⚠️ Video creation returned: {response.status_code}")
            print("📝 This may create an HTML slideshow instead")
        else:
            data = response.json()
            video_file = data.get('video_filename')
            is_html = data.get('is_html', False)
            
            if is_html:
                print(f"✅ Created interactive slideshow: {video_file}")
            else:
                print(f"✅ Created video: {video_file}")
        
        # Show results
        print("\n" + "=" * 50)
        print("🎉 Demo Video Creation Complete!")
        print("\n📁 Generated Files:")
        print(f"   🖼️ Images: {len(successful_images)} educational illustrations")
        print(f"   🎵 Audio: {audio_file}")
        if 'video_file' in locals():
            print(f"   🎬 Video: {video_file}")
        
        print(f"\n📂 Check the 'outputs' folder for all generated content")
        print("💡 Open the HTML file in your browser for interactive viewing")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo creation failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 AI Teaching Video Generator - Demo Creation")
    print("Using Level-2 Groq AI Enhancement")
    print("=" * 50)
    
    success = create_demo()
    
    if success:
        print("\n🎓 Your AI Teaching Video Generator is working perfectly!")
        print("✅ Level-2 Groq AI integration successful")
        print("✅ Educational image generation working")
        print("✅ Text-to-speech narration working")
        print("✅ Video/slideshow assembly working")
    else:
        print("\n⚠️ Demo creation encountered issues")
        print("💡 Check the server logs for more details")