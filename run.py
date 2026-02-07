#!/usr/bin/env python3
"""
AI Teaching Video Generator - Startup Script
Run this file to start the application
"""

import os
import sys
from app import app

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask', 'pyttsx3', 'moviepy', 'requests', 'PIL'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'PIL':
                import PIL
            else:
                __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def create_directories():
    """Create necessary directories"""
    import config
    
    directories = [
        config.UPLOAD_FOLDER,
        config.OUTPUT_FOLDER,
        config.TEMP_FOLDER
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory ready: {directory}")

def main():
    """Main startup function"""
    print("🎓 AI Teaching Video Generator")
    print("=" * 50)
    
    # Check dependencies
    print("🔍 Checking dependencies...")
    if not check_dependencies():
        sys.exit(1)
    
    print("✅ All dependencies found!")
    
    # Create directories
    print("\n📁 Setting up directories...")
    create_directories()
    
    # Check HuggingFace API key
    import config
    if not config.HUGGINGFACE_API_KEY or config.HUGGINGFACE_API_KEY == "your_huggingface_api_key_here":
        print("\n⚠️  Warning: HuggingFace API key not configured!")
        print("   Image generation will not work without a valid API key.")
        print("   Please update config.py with your HuggingFace API key.")
    else:
        print("✅ HuggingFace API key configured!")
    
    # Start the application
    print("\n🚀 Starting AI Teaching Video Generator...")
    print("📱 Open your browser to: http://localhost:5000")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n👋 Shutting down gracefully...")
        sys.exit(0)

if __name__ == '__main__':
    main()