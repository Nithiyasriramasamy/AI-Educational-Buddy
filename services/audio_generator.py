import os
import pyttsx3

def generate_narration(text, output_dir):
    """
    Generates audio narration from text using pyttsx3.
    Returns the filename of the generated audio.
    """
    try:
        print("Initializing TTS engine...")
        engine = pyttsx3.init()
        
        # Configure properties
        engine.setProperty('rate', 150)    # Speed percent (can go over 100)
        engine.setProperty('volume', 0.9)  # Volume 0-1
        
        # Try to select a good voice
        voices = engine.getProperty('voices')
        # Prefer a female voice if available, often clearer for narration
        for voice in voices:
            if "female" in voice.name.lower() or "zira" in voice.name.lower():
                engine.setProperty('voice', voice.id)
                break
        
        filename = "narration.mp3"
        filepath = os.path.join(output_dir, filename)
        
        print(f"Saving audio to {filepath}...")
        # specific to pyttsx3, save_to_file processes the event loop
        engine.save_to_file(text, filepath)
        engine.runAndWait()
        
        return filename
        
    except Exception as e:
        print(f"Error generating audio: {e}")
        return None
