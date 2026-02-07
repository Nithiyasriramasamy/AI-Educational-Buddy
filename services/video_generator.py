import os
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

def create_video(images_dir, audio_path, output_path, scene_count):
    """
    Combines images and audio into a final video.
    """
    try:
        print("Starting video creation...")
        
        # Load audio to get duration
        audio_clip = AudioFileClip(audio_path)
        total_duration = audio_clip.duration
        
        # Calculate duration per image
        # In a real app, we might want timing per scene, but for MVP we split equally
        if scene_count == 0:
            raise ValueError("Scene count is zero")
            
        duration_per_scene = total_duration / scene_count
        print(f"Total duration: {total_duration}s, Scenes: {scene_count}, Duration/scene: {duration_per_scene}s")
        
        image_clips = []
        for i in range(1, scene_count + 1):
            # Check for various image formats
            found_img = None
            # Find the most recent image for this scene
            found_img = None
            candidates = []
            
            # search for files starting with scene_{i}_ or scene_{i}.
            prefix_timestamp = f"scene_{i}_"
            prefix_exact = f"scene_{i}."
            
            try:
                for fname in os.listdir(images_dir):
                    if (fname.startswith(prefix_timestamp) or fname.startswith(prefix_exact)) and \
                       fname.lower().endswith(('.jpg', '.jpeg', '.png')):
                        candidates.append(os.path.join(images_dir, fname))
                
                # Sort by modification time (newest first) to get the latest generation
                if candidates:
                    candidates.sort(key=os.path.getmtime, reverse=True)
                    found_img = candidates[0]
                    print(f"Using image for scene {i}: {os.path.basename(found_img)}")
            except Exception as e:
                print(f"Error searching for images: {e}")
            
            if found_img:
                # Create basic clip
                clip = ImageClip(found_img).set_duration(duration_per_scene)
                
                # Apply Ken Burns effect (Zoom In)
                # Zoom from 100% to 110% over the duration
                try:
                    # Center cropping to maintain aspect ratio while zooming
                    # We simply resize the clip to be slightly larger over time
                    # and keep it centered (default behavior of resize)
                    clip = clip.resize(lambda t: 1 + 0.04 * t)
                    
                    # Alternatively, for better quality but slower:
                    # w, h = clip.size
                    # clip = clip.crop(x1=lambda t: int(w*0.02*t),
                    #                  y1=lambda t: int(h*0.02*t),
                    #                  width=lambda t: int(w*(1-0.04*t)),
                    #                  height=lambda t: int(h*(1-0.04*t)))
                    # But resize is often smoother for simple implementation
                except Exception as e:
                    print(f"Failed to apply zoom effect to scene {i}: {e}")
                
                image_clips.append(clip)
            else:
                print(f"Warning: Image for scene {i} not found (checked jpg, jpeg, png)")
        
        if not image_clips:
            raise ValueError("No images found to create video")
            
        print("Concatenating video clips...")
        # Use overlap for smoother transitions if desired, but simple concat for now
        final_video = concatenate_videoclips(image_clips, method="compose")
        
        print("Setting audio...")
        final_video = final_video.set_audio(audio_clip)
        
        # Ensure the video is the exact length of the audio/slides
        final_video = final_video.set_duration(total_duration)
        
        print(f"Writing video file to {output_path}...")
        final_video.write_videofile(
            output_path, 
            fps=24, 
            codec='libx264', 
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        return True
        
    except Exception as e:
        print(f"Error creating video: {e}")
        return False
