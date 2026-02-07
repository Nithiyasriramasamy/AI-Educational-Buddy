#!/usr/bin/env python3
"""
Test script for AI Teaching Video Generator
Tests core functionality without full video generation
"""

import requests
import json
import time

# Test configuration
BASE_URL = "http://localhost:5000"
TEST_SCRIPT = """First, let's understand what photosynthesis is. Photosynthesis is the process by which plants convert sunlight into energy.

Next, we'll explore the key components needed for photosynthesis. Plants need three main things: sunlight, water, and carbon dioxide.

Finally, we'll discuss why photosynthesis is important. This process not only feeds the plant but also produces the oxygen we breathe."""

def test_split_script():
    """Test script splitting functionality"""
    print("🧪 Testing script splitting...")
    
    response = requests.post(f"{BASE_URL}/split-script", 
                           json={"script": TEST_SCRIPT})
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            scenes = data.get('scenes', [])
            print(f"✅ Script split into {len(scenes)} scenes")
            for i, scene in enumerate(scenes, 1):
                print(f"   Scene {i}: {scene[:50]}...")
            return scenes
        else:
            print(f"❌ Error: {data.get('error')}")
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def test_generate_prompts(scenes):
    """Test prompt generation functionality"""
    print("\n🧪 Testing prompt generation...")
    
    response = requests.post(f"{BASE_URL}/generate-prompts", 
                           json={"scenes": scenes})
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            prompts = data.get('prompts', [])
            print(f"✅ Generated {len(prompts)} prompts")
            for prompt in prompts:
                print(f"   Scene {prompt['scene_number']}: {prompt['prompt'][:60]}...")
            return prompts
        else:
            print(f"❌ Error: {data.get('error')}")
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def test_generate_audio():
    """Test audio generation functionality"""
    print("\n🧪 Testing audio generation...")
    
    response = requests.post(f"{BASE_URL}/generate-audio", 
                           json={"script": TEST_SCRIPT})
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            audio_file = data.get('audio_filename')
            print(f"✅ Audio generated: {audio_file}")
            return audio_file
        else:
            print(f"❌ Error: {data.get('error')}")
            return None
    else:
        print(f"❌ HTTP Error: {response.status_code}")
        return None

def main():
    """Run all tests"""
    print("🎓 AI Teaching Video Generator - Test Suite")
    print("=" * 50)
    
    # Test 1: Script splitting
    scenes = test_split_script()
    if not scenes:
        print("❌ Script splitting failed. Stopping tests.")
        return
    
    # Test 2: Prompt generation
    prompts = test_generate_prompts(scenes)
    if not prompts:
        print("❌ Prompt generation failed. Stopping tests.")
        return
    
    # Test 3: Audio generation
    audio_file = test_generate_audio()
    if not audio_file:
        print("❌ Audio generation failed.")
    
    print("\n" + "=" * 50)
    print("🎉 Core functionality tests completed!")
    print("\n📝 Test Summary:")
    print(f"   ✅ Script splitting: {len(scenes)} scenes")
    print(f"   ✅ Prompt generation: {len(prompts)} prompts")
    print(f"   {'✅' if audio_file else '❌'} Audio generation: {'Success' if audio_file else 'Failed'}")
    
    print("\n💡 Next steps:")
    print("   1. Open http://localhost:5000 in your browser")
    print("   2. Paste the test script and try the full workflow")
    print("   3. Check the outputs/ folder for generated files")

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to the application.")
        print("   Make sure the server is running with: python run.py")
    except Exception as e:
        print(f"❌ Test failed with error: {e}")