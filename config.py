# Configuration settings for AI Teaching Video Generator

import os

# HuggingFace API Configuration
HUGGINGFACE_API_KEY = os.environ.get("HF_TOKEN")
HUGGINGFACE_MODEL = "runwayml/stable-diffusion-v1-5"  # More reliable model

# Groq API Configuration
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
USE_GROQ_ENHANCEMENT = True

# Image Generation Settings
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 768
NUM_INFERENCE_STEPS = 20
GUIDANCE_SCALE = 7.5

# Audio Settings
TTS_RATE = 150  # Words per minute
TTS_VOICE_ID = 0  # Voice selection (0 = default)

# Video Settings
VIDEO_FPS = 1  # Frames per second (1 = 1 second per image)
VIDEO_FORMAT = "mp4"

# File Paths
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"
TEMP_FOLDER = "temp"

# Template for educational prompts (Level-1 approach)
EDUCATIONAL_PROMPT_TEMPLATE = (
    "Educational illustration explaining {concept}, simple flat design, "
    "white background, teaching slide style, student friendly, "
    "clear visual elements, no long text, high clarity"
)

# Scene splitting keywords (used to identify scene breaks)
SCENE_BREAK_KEYWORDS = [
    "Next,", "Now,", "First,", "Second,", "Third,", "Finally,", 
    "Let's", "Consider", "For example", "Another", "Moving on",
    "Step 1", "Step 2", "Step 3", "Chapter", "Section"
]