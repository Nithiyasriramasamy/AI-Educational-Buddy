#!/usr/bin/env python3
"""
Test video creation functionality directly
"""

import os
import sys
from datetime import datetime

# Add current directory to path to import our modules
sys.path.append('.')

from app import TeachingVideoGenerator
import config

def create_test_content():
    """Create test images and audio for video creation"""
    print("🎨 Creating test content...")
    
    generator = TeachingVideoGenerator()
    
    # Create test images using fallback method
    test_images = []
    for i in range(3):
        prompt = f"Educational illustration explaining test concept {i+1}, simple flat design, white background, teaching slide style"
        image_data = generator.create_fallback_image(prompt, i+1)
        
        if image_data:
            filename = f"test_image_{i+1}.png"
            filepath = os.path.join(config.OUTPUT_FOLDER, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            test_images.append(filepath)
            print(f"   ✅ Created: {filename}")
    
    # Create test audio
    test_script = "This is a test narration for our teaching video. First, we learn about concept one. Next, we explore concept two. Finally, we understand concept three."
    
    audio_filename = "test_narration.mp3"
    audio_path = os.path.join(config.OUTPUT_FOLDER, audio_filename)
    
    success = generator.generate_narration_audio(test_script, audio_path)
    
    if success and os.path.exists(audio_path):
        print(f"   ✅ Created: {audio_filename}")
        return test_images, audio_path
    else:
        print("   ❌ Failed to create audio")
        return test_images, None

def test_video_creation():
    """Test the video creation functionality"""
    print("🎬 Testing Video Creation")
    print("=" * 50)
    
    # Create test content
    image_paths, audio_path = create_test_content()
    
    if not image_paths:
        print("❌ No test images created")
        return False
    
    if not audio_path:
        print("❌ No test audio created")
        return False
    
    # Test video creation
    generator = TeachingVideoGenerator()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"test_video_{timestamp}.mp4"
    video_path = os.path.join(config.OUTPUT_FOLDER, video_filename)
    
    print(f"\n🎥 Creating video: {video_filename}")
    print(f"   Images: {len(image_paths)}")
    print(f"   Audio: {os.path.basename(audio_path)}")
    
    success = generator.create_teaching_video(image_paths, audio_path, video_path)
    
    if success:
        # Check what was actually created
        if os.path.exists(video_path):
            size = os.path.getsize(video_path)
            print(f"✅ MP4 video created: {video_filename} ({size} bytes)")
            return video_filename
        
        # Check for HTML slideshow
        html_path = video_path.replace('.mp4', '.html')
        if os.path.exists(html_path):
            print(f"✅ HTML slideshow created: {os.path.basename(html_path)}")
            return os.path.basename(html_path)
        
        print("❌ No output file found")
        return False
    else:
        print("❌ Video creation failed")
        return False

def main():
    """Main test function"""
    print("🧪 Video Creation Test Suite")
    print("=" * 50)
    
    # Ensure directories exist
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    os.makedirs(config.TEMP_FOLDER, exist_ok=True)
    
    # Test video creation
    result = test_video_creation()
    
    print("\n" + "=" * 50)
    if result:
        print(f"🎉 Success! Created: {result}")
        print(f"📁 Check the outputs folder: {config.OUTPUT_FOLDER}")
        
        if result.endswith('.html'):
            print("💡 Open the HTML file in your browser to view the slideshow")
        else:
            print("💡 Play the MP4 file in any video player")
            
        print("\n🚀 The video creation is now working!")
        print("   You can use the web interface at http://localhost:5000")
    else:
        print("❌ Video creation test failed")
        print("💡 Check the console output above for error details")

if __name__ == "__main__":
    main()