# AI Teaching Video Generator - Setup Guide

## Quick Start

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure HuggingFace API Key**
   - Open `config.py`
   - Replace the placeholder with your actual HuggingFace API key
   - Your key: `HF_TOKEN="xxx"`

3. **Run the Application**
   ```bash
   python run.py
   ```

4. **Open Browser**
   - Navigate to `http://localhost:5000`
   - Start creating teaching videos!

## Detailed Installation

### System Requirements
- Python 3.8 or higher
- Windows/macOS/Linux
- 4GB RAM minimum (8GB recommended)
- Internet connection for image generation

### Dependencies Explained

**Core Framework:**
- `flask` - Web framework for the backend API
- `requests` - HTTP library for HuggingFace API calls

**Media Processing:**
- `pyttsx3` - Text-to-speech engine (offline)
- `moviepy` - Video editing and creation
- `pillow` - Image processing and manipulation

**Data Processing:**
- `numpy` - Numerical computations (required by moviepy)

### Configuration Options

Edit `config.py` to customize:

**Image Generation:**
```python
IMAGE_WIDTH = 1024          # Generated image width
IMAGE_HEIGHT = 768          # Generated image height
NUM_INFERENCE_STEPS = 20    # Quality vs speed (10-50)
GUIDANCE_SCALE = 7.5        # Prompt adherence (1-20)
```

**Audio Settings:**
```python
TTS_RATE = 150             # Words per minute (100-200)
TTS_VOICE_ID = 0           # Voice selection (0-N)
```

**Video Settings:**
```python
VIDEO_FPS = 1              # Frames per second
VIDEO_FORMAT = "mp4"       # Output format
```

## Troubleshooting

### Common Issues

**1. TTS Not Working (Windows)**
```bash
# Install additional TTS engines
pip install pyttsx3[win32]
```

**2. MoviePy Installation Issues**
```bash
# Install with specific version
pip install moviepy==1.0.3
# Or try development version
pip install git+https://github.com/Zulko/moviepy.git
```

**3. HuggingFace API Errors**
- Check your API key is valid
- Ensure you have sufficient quota
- Try a different model in `config.py`

**4. Memory Issues**
- Reduce `IMAGE_WIDTH` and `IMAGE_HEIGHT`
- Process fewer scenes at once
- Close other applications

### Performance Optimization

**For Faster Image Generation:**
- Use smaller image dimensions (512x384)
- Reduce `NUM_INFERENCE_STEPS` to 10-15
- Consider local Stable Diffusion setup

**For Better Quality:**
- Increase `NUM_INFERENCE_STEPS` to 30-50
- Use higher resolution (1024x768 or larger)
- Adjust `GUIDANCE_SCALE` for prompt adherence

## Advanced Setup

### Local Stable Diffusion (Optional)

For offline image generation, you can set up local Stable Diffusion:

1. **Install AUTOMATIC1111 WebUI**
   ```bash
   git clone https://github.com/AUTOMATIC1111/stable-diffusion-webui.git
   cd stable-diffusion-webui
   ./webui.sh --api
   ```

2. **Update config.py**
   ```python
   # Use local API instead of HuggingFace
   USE_LOCAL_SD = True
   LOCAL_SD_URL = "http://127.0.0.1:7860"
   ```

### Custom TTS Voices

**Windows:**
- Install additional SAPI voices
- Update `TTS_VOICE_ID` in config.py

**macOS:**
- Use built-in System Voices
- Configure in System Preferences > Accessibility > Speech

**Linux:**
- Install espeak or festival
- Configure pyttsx3 engine

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "run.py"]
```

## File Structure

```
ai-teaching-video-generator/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── utils.py              # Utility functions
├── examples.py           # Example teaching scripts
├── run.py                # Startup script
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── SETUP.md             # This setup guide
├── templates/           # HTML templates
│   ├── base.html
│   └── index.html
├── static/              # CSS and JavaScript
│   ├── style.css
│   └── script.js
├── uploads/             # User uploaded files
├── outputs/             # Generated content
└── temp/                # Temporary processing files
```

## Next Steps

1. **Test with Example Scripts**
   - Use the provided examples in `examples.py`
   - Try different script lengths and styles

2. **Customize Prompts**
   - Modify `EDUCATIONAL_PROMPT_TEMPLATE` in `config.py`
   - Experiment with different visual styles

3. **Upgrade to Level-2**
   - Integrate LLM for prompt enhancement
   - Add scene analysis capabilities
   - Implement custom prompt refinement

## Support

For issues and questions:
1. Check this setup guide
2. Review error messages in the console
3. Test with example scripts first
4. Verify all dependencies are installed correctly