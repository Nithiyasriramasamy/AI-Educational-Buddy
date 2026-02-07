#!/usr/bin/env python3
"""
Test image generation functionality
"""

import requests
import json

def test_image_generation():
    """Test the fixed image generation"""
    
    # Test data
    test_prompts = [
        {
            "scene_number": 1,
            "scene_text": "First, let's understand what photosynthesis is.",
            "concept": "photosynthesis process plants convert sunlight",
            "prompt": "Educational illustration explaining photosynthesis process plants convert sunlight, simple flat design, white background, teaching slide style, student friendly, clear visual elements, no long text, high clarity"
        }
    ]
    
    print("🧪 Testing Image Generation Fix...")
    print("=" * 50)
    
    try:
        response = requests.post(
            "http://localhost:5000/generate-images",
            json={"prompts": test_prompts},
            timeout=120  # 2 minutes timeout
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                images = data.get('images', [])
                for img in images:
                    if img.get('error'):
                        print(f"❌ Scene {img['scene_number']}: {img['error']}")
                    else:
                        print(f"✅ Scene {img['scene_number']}: Image generated successfully!")
                        print(f"   Filename: {img.get('filename', 'N/A')}")
                        if img.get('image_data'):
                            print(f"   Data size: {len(img['image_data'])} characters")
                
                return len([img for img in images if not img.get('error')]) > 0
            else:
                print(f"❌ API Error: {data.get('error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out - this is normal for first API calls")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_image_generation()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 Image generation is working!")
        print("💡 Try the web interface again at http://localhost:5000")
    else:
        print("⚠️  Image generation still has issues")
        print("💡 The app will use fallback images instead")
        print("   Fallback images are educational-style placeholders")
    
    print("\n📝 Note: HuggingFace API can be slow on first requests")
    print("   If it fails, the app automatically creates fallback images")