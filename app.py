import os
import time
from flask import Flask, render_template, request, jsonify, send_from_directory
from dotenv import load_dotenv

# Import our modules
import utils.prompt_generator_groq as groq_utils
import services.groq_prompt_generator as groq_generator
import utils.script_splitter as script_utils
import services.nvidia_image_generator as image_gen
import services.audio_generator as audio_gen
import services.video_generator as video_gen
import attention_detector

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Configuration
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['STATIC_FOLDER'] = 'static'
app.config['IMAGES_FOLDER'] = os.path.join('static', 'images')
app.config['AUDIO_FOLDER'] = os.path.join('static', 'audio')
app.config['VIDEO_FOLDER'] = os.path.join('static', 'video')

# Ensure directories exist
for folder in [app.config['IMAGES_FOLDER'], app.config['AUDIO_FOLDER'], app.config['VIDEO_FOLDER']]:
    os.makedirs(folder, exist_ok=True)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generator')
def generator():
    return render_template('generator.html')

# API Endpoints
@app.route('/api/topic-to-script', methods=['POST'])
def topic_to_script():
    data = request.json
    topic = data.get('topic')
    profile = data.get('profile') # Get profile from request
    
    if not topic:
        return jsonify({'error': 'Topic is required'}), 400
        
    try:
        script = groq_utils.generate_script_from_topic(topic, profile)
        return jsonify({'script': script})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-prompts', methods=['POST'])
def generate_prompts():
    data = request.json
    script = data.get('script')
    
    if not script:
        return jsonify({'error': 'Script is required'}), 400
        
    try:
        raw_scenes = groq_generator.generate_scene_prompts(script)
        validated_scenes = script_utils.validate_scene_data(raw_scenes)
        return jsonify({'scenes': validated_scenes})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    scenes = data.get('scenes')
    
    if not scenes:
        return jsonify({'error': 'Scenes data is required'}), 400
        
    generated_images = []
    
    try:
        # Generate an image for each scene
        for scene in scenes:
            scene_num = scene.get('scene_number')
            prompt = scene.get('image_prompt')
            
            filename = image_gen.generate_scene_image(
                prompt, 
                scene_num, 
                app.config['IMAGES_FOLDER']
            )
            
            if filename:
                # Add timestamp to bypass browser cache
                url = f"/static/images/{filename}?t={int(time.time())}"
                generated_images.append({
                    'scene_number': scene_num,
                    'url': url
                })
        
        if not generated_images:
            return jsonify({'error': 'Failed to generate any images'}), 500
            
        return jsonify({'images': generated_images})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/generate-audio', methods=['POST'])
def generate_audio():
    data = request.json
    script = data.get('script')
    
    if not script:
        return jsonify({'error': 'Script is required'}), 400
        
    try:
        # Clean script for TTS
        clean_text = script_utils.clean_script_text(script)
        
        filename = audio_gen.generate_narration(
            clean_text, 
            app.config['AUDIO_FOLDER']
        )
        
        if filename:
            url = f"/static/audio/{filename}?t={int(time.time())}"
            return jsonify({'audio_url': url})
        else:
            return jsonify({'error': 'Failed to generate audio'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/create-video', methods=['POST'])
def create_video_endpoint():
    data = request.json
    scene_count = data.get('scene_count')
    
    try:
        audio_path = os.path.join(app.config['AUDIO_FOLDER'], "narration.mp3")
        output_filename = "output.mp4"
        output_path = os.path.join(app.config['VIDEO_FOLDER'], output_filename)
        
        success = video_gen.create_video(
            app.config['IMAGES_FOLDER'],
            audio_path,
            output_path,
            scene_count
        )
        
        if success:
            url = f"/static/video/{output_filename}?t={int(time.time())}"
            return jsonify({'video_url': url})
        else:
            return jsonify({'error': 'Failed to create video'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/quiz')
def quiz():
    return render_template('quiz.html')

@app.route('/api/analyze-quiz', methods=['POST'])
def analyze_quiz():
    data = request.json
    answers = data.get('answers', [])
    
    # Analyze conversational traits
    interest_score = 0
    comfort_score = 0
    style_pref = "balanced" # 'stories', 'balanced', 'concepts'
    
    for item in answers:
        ans = item['answer'].lower()
        
        # Interest signals
        if any(w in ans for w in ['cool', 'excited', 'wow', 'instantly']):
            interest_score += 2
        elif any(w in ans for w in ['interesting', 'curious', 'ask']):
            interest_score += 1
        elif any(w in ans for w in ['boring', 'confusing', 'scary', 'care']):
            interest_score -= 1
            
        # Comfort signals
        if any(w in ans for w in ['deep', 'reasons', 'more']):
            comfort_score += 2
        elif any(w in ans for w in ['simple', 'video', 'scared', 'complicated']):
            comfort_score -= 1
            
        # Learning Style (direct question)
        if "stories" in ans:
            style_pref = "stories"
        elif "facts" in ans:
            style_pref = "balanced"
        elif "deep" in ans or "reasons" in ans:
            style_pref = "concepts"
        elif "video" in ans:
            style_pref = "visual"

    # Determine explanation based on profile
    explanation = ""
    curiosity_question = ""
    
    if comfort_score < 0: # Prefers simple/safe
        explanation = "Don't worry, it sounds more complicated than it is! Think of gravity like a giant magnet in the ground that pulls us down. Anti-gravity would simply be a way to 'turn off' that magnet for a second, letting us float freely like an astronaut in space. It’s a fun idea because it would make moving heavy things super easy!"
        curiosity_question = "If you could turn off gravity for just 5 minutes, what would you do first?"
        
    elif comfort_score > 2 or style_pref == "concepts": # Loves deep thoughts
        explanation = "I love that you're thinking about the 'why'! Scientists see gravity as the bending of space itself—like a heavy ball curving a trampoline. Anti-gravity would mean bending space the *opposite* way, pushing things apart instead of pulling them together. It challenges everything we know about how the universe is built!"
        curiosity_question = "Do you think we'll ever find a way to 'push' against space itself?"
        
    elif style_pref == "stories" or style_pref == "visual":
        explanation = "Imagine you're wearing a backpack, but instead of weighing you down, it gently lifts you up. That's the dream of anti-gravity! It's like the hoverboards in movies. Instead of fighting against the earth's pull with loud rockets, we would just gently drift away. It would change how we travel forever."
        curiosity_question = "What kind of vehicle would you build if it didn't need wheels or wings?"
        
    else: # Balanced / Default
        explanation = "It's a really cool concept. Basically, gravity is the force that pulls everything together. Anti-gravity is the idea of a force that pushes things apart. While we can't do it yet, scientists study things like magnetic fields to see if we can mimic it. It helps us understand the rules of nature better."
        curiosity_question = "If you had a floating car, where is the first place you'd visit?"

    return jsonify({
        'explanation': explanation,
        'question': curiosity_question,
        'profile': {
            'interest': interest_score,
            'comfort': comfort_score,
            'style': style_pref
        }
    })

@app.route('/attention')
def attention_demo():
    # Start the background detection thread when this page is accessed
    attention_detector.detector.start()
    return render_template('attention.html')

@app.route('/attention-status')
def get_attention_status():
    status = attention_detector.detector.get_status()
    return jsonify({'status': status})

if __name__ == '__main__':
    print("Starting AI Teaching Video Generator...")
    print("Make sure you have set GROQ_API_KEY and NVIDIA_API_KEY in your .env file")
    app.run(debug=True, port=5000)
