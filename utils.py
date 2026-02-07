"""
Utility functions for AI Teaching Video Generator
"""

import os
import re
import json
from datetime import datetime
from typing import List, Dict, Any

def clean_filename(filename: str) -> str:
    """Clean filename to be filesystem-safe"""
    # Remove or replace invalid characters
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove extra spaces and dots
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'\.+', '.', filename)
    # Limit length
    if len(filename) > 100:
        name, ext = os.path.splitext(filename)
        filename = name[:95] + ext
    return filename

def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract key concepts from text for prompt generation"""
    # Common stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those',
        'we', 'you', 'they', 'it', 'he', 'she', 'i', 'me', 'us', 'them', 'him', 'her'
    }
    
    # Extract words and filter
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    keywords = [word for word in words if word not in stop_words]
    
    # Count frequency and get most common
    word_freq = {}
    for word in keywords:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    return [word for word, freq in sorted_words[:max_keywords]]

def validate_script_content(script: str) -> Dict[str, Any]:
    """Validate script content and provide feedback"""
    result = {
        'valid': True,
        'warnings': [],
        'suggestions': [],
        'stats': {}
    }
    
    # Basic stats
    word_count = len(script.split())
    sentence_count = len(re.findall(r'[.!?]+', script))
    paragraph_count = len([p for p in script.split('\n\n') if p.strip()])
    
    result['stats'] = {
        'word_count': word_count,
        'sentence_count': sentence_count,
        'paragraph_count': paragraph_count,
        'estimated_duration': word_count / 150  # Assuming 150 WPM
    }
    
    # Validation checks
    if word_count < 50:
        result['warnings'].append("Script is quite short. Consider adding more content for better video quality.")
    
    if word_count > 2000:
        result['warnings'].append("Script is very long. Consider breaking it into multiple videos.")
    
    if paragraph_count < 2:
        result['suggestions'].append("Consider breaking your script into multiple paragraphs for better scene division.")
    
    if sentence_count < 5:
        result['warnings'].append("Very few sentences detected. This may result in limited scenes.")
    
    # Check for educational keywords
    educational_keywords = ['learn', 'understand', 'explain', 'example', 'concept', 'theory', 'practice']
    found_keywords = [kw for kw in educational_keywords if kw in script.lower()]
    
    if not found_keywords:
        result['suggestions'].append("Consider adding educational keywords like 'learn', 'understand', 'explain' to improve teaching effectiveness.")
    
    return result

def format_duration(seconds: float) -> str:
    """Format duration in seconds to human-readable format"""
    if seconds < 60:
        return f"{seconds:.1f} seconds"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f} minutes"
    else:
        hours = seconds / 3600
        return f"{hours:.1f} hours"

def log_generation_stats(stats: Dict[str, Any], log_file: str = "generation_log.json"):
    """Log generation statistics for analysis"""
    try:
        # Load existing log
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        else:
            log_data = {'generations': []}
        
        # Add timestamp
        stats['timestamp'] = datetime.now().isoformat()
        
        # Append new stats
        log_data['generations'].append(stats)
        
        # Keep only last 100 entries
        if len(log_data['generations']) > 100:
            log_data['generations'] = log_data['generations'][-100:]
        
        # Save log
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
            
    except Exception as e:
        print(f"Warning: Could not log generation stats: {e}")

def get_file_size_mb(filepath: str) -> float:
    """Get file size in megabytes"""
    try:
        size_bytes = os.path.getsize(filepath)
        return size_bytes / (1024 * 1024)
    except:
        return 0.0

def cleanup_temp_files(temp_dir: str, max_age_hours: int = 24):
    """Clean up temporary files older than specified hours"""
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600
        
        for filename in os.listdir(temp_dir):
            filepath = os.path.join(temp_dir, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"Cleaned up old temp file: {filename}")
                    
    except Exception as e:
        print(f"Warning: Could not clean up temp files: {e}")

def estimate_processing_time(word_count: int, scene_count: int) -> Dict[str, float]:
    """Estimate processing time for different stages"""
    return {
        'script_analysis': 2,  # seconds
        'prompt_generation': scene_count * 0.5,  # 0.5 seconds per scene
        'image_generation': scene_count * 15,  # 15 seconds per image (API dependent)
        'audio_generation': word_count / 150 * 2,  # 2x real-time for TTS
        'video_creation': scene_count * 3,  # 3 seconds per scene for video processing
    }

def validate_huggingface_response(response_data: bytes) -> bool:
    """Validate HuggingFace API response"""
    try:
        # Check if response looks like image data
        if len(response_data) < 1000:  # Too small to be an image
            return False
        
        # Check for common image headers
        image_headers = [
            b'\x89PNG',  # PNG
            b'\xff\xd8\xff',  # JPEG
            b'GIF8',  # GIF
            b'RIFF'  # WebP
        ]
        
        return any(response_data.startswith(header) for header in image_headers)
        
    except:
        return False

def create_fallback_image(width: int = 1024, height: int = 768, text: str = "Image Generation Failed") -> bytes:
    """Create a fallback image when generation fails"""
    try:
        from PIL import Image, ImageDraw, ImageFont
        import io
        
        # Create image
        img = Image.new('RGB', (width, height), color='lightgray')
        draw = ImageDraw.Draw(img)
        
        # Try to use a font, fallback to default
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2
        
        # Draw text
        draw.text((x, y), text, fill='black', font=font)
        
        # Convert to bytes
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        return img_bytes.getvalue()
        
    except Exception as e:
        print(f"Could not create fallback image: {e}")
        return b''