#!/usr/bin/env python3
"""
Test and fix audio generation issues
"""

import os
import sys
import pyttsx3
import subprocess
import tempfile
import wave
import struct

# Add current directory to path
sys.path.append('.')
import config

def test_pyttsx3():
    """Test pyttsx3 TTS engine"""
    print("🔍 Testing pyttsx3...")
    
    try:
        # Initialize engine
        engine = pyttsx3.init()
        
        # Get available voices
        voices = engine.getProperty('voices')
        print(f"   Available voices: {len(voices) if voices else 0}")
        
        if voices:
            for i, voice in enumerate(voices[:3]):  # Show first 3
                print(f"   Voice {i}: {voice.name if hasattr(voice, 'name') else 'Unknown'}")
        
        # Test audio generation
        test_text = "This is a test of the text to speech system."
        test_file = os.path.join(config.OUTPUT_FOLDER, "test_pyttsx3.wav")
        
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        engine.save_to_file(test_text, test_file)
        engine.runAndWait()
        
        if os.path.exists(test_file) and os.path.getsize(test_file) > 100:
            print("   ✅ pyttsx3 working!")
            return True
        else:
            print("   ❌ pyttsx3 failed to create audio file")
            return False
            
    except Exception as e:
        print(f"   ❌ pyttsx3 error: {e}")
        return False

def test_windows_sapi():
    """Test Windows SAPI directly"""
    print("🔍 Testing Windows SAPI...")
    
    try:
        test_text = "This is a test of Windows Speech API."
        test_file = os.path.join(config.OUTPUT_FOLDER, "test_sapi.wav")
        
        # Create VBS script
        vbs_script = f'''
Set objVoice = CreateObject("SAPI.SpVoice")
Set objFileStream = CreateObject("SAPI.SpFileStream")

objFileStream.Open "{test_file.replace('/', '\\')}", 3
Set objVoice.AudioOutputStream = objFileStream

objVoice.Rate = 0
objVoice.Volume = 90

objVoice.Speak "{test_text}"

objFileStream.Close
Set objVoice = Nothing
Set objFileStream = Nothing
'''
        
        # Write and run VBS script
        with tempfile.NamedTemporaryFile(mode='w', suffix='.vbs', delete=False) as f:
            f.write(vbs_script)
            vbs_path = f.name
        
        result = subprocess.run(['cscript', '//NoLogo', vbs_path], 
                              capture_output=True, text=True, timeout=30)
        
        # Clean up
        try:
            os.unlink(vbs_path)
        except:
            pass
        
        if os.path.exists(test_file) and os.path.getsize(test_file) > 100:
            print("   ✅ Windows SAPI working!")
            return True
        else:
            print("   ❌ Windows SAPI failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Windows SAPI error: {e}")
        return False

def create_silent_audio():
    """Create silent audio as fallback"""
    print("🔍 Testing silent audio creation...")
    
    try:
        test_file = os.path.join(config.OUTPUT_FOLDER, "test_silent.wav")
        
        # Audio parameters
        sample_rate = 22050
        duration = 3  # 3 seconds
        num_samples = int(sample_rate * duration)
        
        # Create WAV file
        with wave.open(test_file, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            
            # Write silence
            for _ in range(num_samples):
                wav_file.writeframes(struct.pack('<h', 0))
        
        if os.path.exists(test_file) and os.path.getsize(test_file) > 100:
            print("   ✅ Silent audio creation working!")
            return True
        else:
            print("   ❌ Silent audio creation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Silent audio error: {e}")
        return False

def test_app_audio_generation():
    """Test the app's audio generation"""
    print("🔍 Testing app audio generation...")
    
    try:
        from app import TeachingVideoGenerator
        
        generator = TeachingVideoGenerator()
        test_script = "This is a test of the teaching video generator audio system. It should create clear narration for educational content."
        test_file = os.path.join(config.OUTPUT_FOLDER, "test_app_audio.mp3")
        
        success = generator.generate_narration_audio(test_script, test_file)
        
        if success:
            # Check if any audio file was created (might be .wav instead of .mp3)
            possible_files = [
                test_file,
                test_file.replace('.mp3', '.wav'),
                os.path.join(config.OUTPUT_FOLDER, "test_app_audio.wav")
            ]
            
            for file_path in possible_files:
                if os.path.exists(file_path) and os.path.getsize(file_path) > 100:
                    print(f"   ✅ App audio generation working! Created: {os.path.basename(file_path)}")
                    return True
            
            print("   ❌ App reported success but no valid audio file found")
            return False
        else:
            print("   ❌ App audio generation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ App audio test error: {e}")
        return False

def fix_audio_issues():
    """Attempt to fix common audio issues"""
    print("🔧 Attempting to fix audio issues...")
    
    try:
        # Reinstall pyttsx3
        print("   📦 Reinstalling pyttsx3...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', '--force-reinstall', 'pyttsx3'], 
                      capture_output=True)
        
        # Install additional Windows TTS components
        print("   🔊 Installing Windows TTS components...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'pywin32'], 
                      capture_output=True)
        
        print("   ✅ Audio components reinstalled")
        return True
        
    except Exception as e:
        print(f"   ❌ Fix attempt failed: {e}")
        return False

def main():
    """Run audio diagnostics and fixes"""
    print("🎵 Audio Generation Diagnostic Tool")
    print("=" * 50)
    
    # Ensure output directory exists
    os.makedirs(config.OUTPUT_FOLDER, exist_ok=True)
    
    # Run tests
    results = {
        'pyttsx3': test_pyttsx3(),
        'sapi': test_windows_sapi(),
        'silent': create_silent_audio(),
        'app': test_app_audio_generation()
    }
    
    print("\n" + "=" * 50)
    print("📊 Audio Test Results:")
    print(f"   pyttsx3 TTS: {'✅ Working' if results['pyttsx3'] else '❌ Failed'}")
    print(f"   Windows SAPI: {'✅ Working' if results['sapi'] else '❌ Failed'}")
    print(f"   Silent Audio: {'✅ Working' if results['silent'] else '❌ Failed'}")
    print(f"   App Integration: {'✅ Working' if results['app'] else '❌ Failed'}")
    
    # Provide recommendations
    print("\n💡 Recommendations:")
    
    if results['app']:
        print("   🎉 Audio generation is working! The app should now create narration.")
    elif results['pyttsx3'] or results['sapi']:
        print("   🔄 Basic TTS is working. Restart the app to apply fixes.")
    elif results['silent']:
        print("   ⚠️ Only silent audio works. The app will create silent placeholders.")
        print("   💡 Try running: pip install --upgrade pyttsx3 pywin32")
    else:
        print("   ❌ All audio methods failed. Manual intervention needed.")
        print("   🔧 Try running the fix function...")
        fix_audio_issues()
    
    print(f"\n📁 Test files created in: {config.OUTPUT_FOLDER}")
    print("🚀 Restart the web application to apply any fixes")

if __name__ == "__main__":
    main()