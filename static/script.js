// AI Teaching Video Generator - Frontend JavaScript

class TeachingVideoApp {
    constructor() {
        this.currentStep = 1;
        this.maxSteps = 5;
        this.scenes = [];
        this.prompts = [];
        this.images = [];
        this.audioFile = null;
        this.videoFile = null;
        
        this.initializeEventListeners();
        this.updateProgress();
        this.loadSystemStatus();
    }
    
    initializeEventListeners() {
        // Step 1: Split Script
        document.getElementById('split-script-btn').addEventListener('click', () => {
            this.splitScript();
        });
        
        // Step 2: Generate Images
        document.getElementById('generate-images-btn').addEventListener('click', () => {
            this.generateImages();
        });
        
        // Step 3: Generate Audio
        document.getElementById('generate-audio-btn').addEventListener('click', () => {
            this.generateAudio();
        });
        
        // Step 4: Create Video
        document.getElementById('create-video-btn').addEventListener('click', () => {
            this.createVideo();
        });
        
        // Level Toggle
        document.getElementById('groq-toggle').addEventListener('change', (e) => {
            this.toggleEnhancement(e.target.checked);
        });
    }
    
    async loadSystemStatus() {
        try {
            const response = await fetch('/get-status');
            const data = await response.json();
            
            if (data.success) {
                const toggle = document.getElementById('groq-toggle');
                const levelText = document.getElementById('current-level');
                const levelDesc = document.getElementById('level-description');
                
                toggle.checked = data.groq_enabled;
                levelText.textContent = data.level;
                
                if (data.groq_enabled) {
                    levelDesc.textContent = "Advanced AI analysis for better educational prompts";
                } else {
                    levelDesc.textContent = "Template-based approach for consistent results";
                }
            }
        } catch (error) {
            console.error('Failed to load system status:', error);
        }
    }
    
    async toggleEnhancement(useGroq) {
        try {
            const response = await fetch('/toggle-enhancement', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ use_groq: useGroq })
            });
            
            const data = await response.json();
            
            if (data.success) {
                const levelText = document.getElementById('current-level');
                const levelDesc = document.getElementById('level-description');
                
                levelText.textContent = data.level;
                
                if (useGroq) {
                    levelDesc.textContent = "Advanced AI analysis for better educational prompts";
                } else {
                    levelDesc.textContent = "Template-based approach for consistent results";
                }
                
                // Show notification
                this.showNotification(`Switched to ${data.level}`, 'success');
            } else {
                throw new Error(data.error || 'Failed to toggle enhancement');
            }
        } catch (error) {
            console.error('Error toggling enhancement:', error);
            this.showNotification('Failed to switch levels', 'error');
        }
    }
    
    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    showLoading(show = true) {
        const spinner = document.getElementById('loading-spinner');
        spinner.style.display = show ? 'block' : 'none';
    }
    
    updateProgress() {
        const progressFill = document.getElementById('progress-fill');
        const progressText = document.getElementById('progress-text');
        
        const percentage = (this.currentStep / this.maxSteps) * 100;
        progressFill.style.width = `${percentage}%`;
        
        const stepTexts = [
            'Ready to start',
            'Script analysis complete',
            'Prompts generated',
            'Images created',
            'Audio generated',
            'Video ready for download'
        ];
        
        progressText.textContent = stepTexts[this.currentStep];
    }
    
    showStep(stepNumber) {
        // Hide all steps
        document.querySelectorAll('.step-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        
        // Show current step
        document.getElementById(`step-${stepNumber}`).classList.add('active');
        
        this.currentStep = stepNumber;
        this.updateProgress();
    }
    
    async splitScript() {
        const scriptText = document.getElementById('script-input').value.trim();
        
        if (!scriptText) {
            alert('Please enter a teaching script first.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/split-script', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ script: scriptText })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.scenes = data.scenes;
                await this.generatePrompts();
            } else {
                throw new Error(data.error || 'Failed to split script');
            }
        } catch (error) {
            console.error('Error splitting script:', error);
            alert('Error splitting script: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    async generatePrompts() {
        try {
            const response = await fetch('/generate-prompts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ scenes: this.scenes })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.prompts = data.prompts;
                this.displayPrompts();
                this.showStep(2);
                
                // Enable generate images button
                document.getElementById('generate-images-btn').disabled = false;
            } else {
                throw new Error(data.error || 'Failed to generate prompts');
            }
        } catch (error) {
            console.error('Error generating prompts:', error);
            alert('Error generating prompts: ' + error.message);
        }
    }
    
    displayPrompts() {
        const container = document.getElementById('prompts-container');
        container.innerHTML = '';
        
        this.prompts.forEach(prompt => {
            const promptElement = document.createElement('div');
            promptElement.className = 'prompt-item';
            
            promptElement.innerHTML = `
                <div class="prompt-header">
                    <span class="scene-number">Scene ${prompt.scene_number}</span>
                </div>
                <div class="scene-text">
                    <strong>Original Text:</strong><br>
                    ${prompt.scene_text}
                </div>
                <div class="prompt-text">
                    <strong>Generated Prompt:</strong><br>
                    ${prompt.prompt}
                </div>
            `;
            
            container.appendChild(promptElement);
        });
    }
    
    async generateImages() {
        if (this.prompts.length === 0) {
            alert('No prompts available. Please generate prompts first.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/generate-images', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ prompts: this.prompts })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.images = data.images;
                this.displayImages();
                this.showStep(3);
                
                // Enable generate audio button
                document.getElementById('generate-audio-btn').disabled = false;
            } else {
                throw new Error(data.error || 'Failed to generate images');
            }
        } catch (error) {
            console.error('Error generating images:', error);
            alert('Error generating images: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayImages() {
        const container = document.getElementById('images-container');
        container.innerHTML = '';
        
        // Create a grid layout for images
        const gridContainer = document.createElement('div');
        gridContainer.style.cssText = `
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        `;
        
        this.images.forEach(image => {
            const imageElement = document.createElement('div');
            imageElement.className = 'image-item';
            imageElement.style.cssText = `
                background: white;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 4px 15px rgba(0,0,0,0.1);
                transition: transform 0.3s;
            `;
            
            if (image.error) {
                imageElement.innerHTML = `
                    <div class="image-error" style="padding: 20px; text-align: center; background: #ffebee; color: #c62828;">
                        <h4>Scene ${image.scene_number}</h4>
                        <p>Error: ${image.error}</p>
                        <p style="font-size: 12px; margin-top: 10px;">Using fallback image generation...</p>
                    </div>
                `;
            } else {
                imageElement.innerHTML = `
                    <div style="position: relative;">
                        <img src="/view/${image.filename}" 
                             alt="Scene ${image.scene_number}" 
                             style="width: 100%; height: 250px; object-fit: cover;">
                        <div style="position: absolute; top: 10px; left: 10px; background: rgba(0,0,0,0.7); color: white; padding: 5px 10px; border-radius: 15px; font-size: 12px; font-weight: bold;">
                            Scene ${image.scene_number}
                        </div>
                    </div>
                    <div class="image-info" style="padding: 15px;">
                        <h4 style="margin: 0 0 8px 0; color: #333;">Scene ${image.scene_number}</h4>
                        <p style="margin: 0; color: #666; font-size: 14px;">✅ Generated successfully</p>
                        <button onclick="window.open('/view/${image.filename}', '_blank')" 
                                style="margin-top: 10px; padding: 5px 10px; background: #667eea; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 12px;">
                            🔍 View Full Size
                        </button>
                    </div>
                `;
            }
            
            // Add hover effect
            imageElement.addEventListener('mouseenter', () => {
                imageElement.style.transform = 'translateY(-5px)';
            });
            imageElement.addEventListener('mouseleave', () => {
                imageElement.style.transform = 'translateY(0)';
            });
            
            gridContainer.appendChild(imageElement);
        });
        
        container.appendChild(gridContainer);
        
        // Add summary info
        const summaryDiv = document.createElement('div');
        summaryDiv.style.cssText = `
            text-align: center;
            padding: 20px;
            background: #e8f5e8;
            border-radius: 8px;
            margin-top: 20px;
        `;
        
        const successCount = this.images.filter(img => !img.error).length;
        const totalCount = this.images.length;
        
        summaryDiv.innerHTML = `
            <h4 style="margin: 0 0 10px 0; color: #2e7d32;">
                🎨 Image Generation Complete
            </h4>
            <p style="margin: 0; color: #388e3c;">
                Successfully generated ${successCount} out of ${totalCount} images
            </p>
            ${successCount < totalCount ? 
                `<p style="margin: 5px 0 0 0; color: #f57c00; font-size: 14px;">
                    ${totalCount - successCount} images used fallback generation (still looks great!)
                </p>` : ''
            }
        `;
        
        container.appendChild(summaryDiv);
    }
    
    async generateAudio() {
        const scriptText = document.getElementById('script-input').value.trim();
        
        if (!scriptText) {
            alert('No script text available.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/generate-audio', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ script: scriptText })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.audioFile = data.audio_filename;
                this.displayAudio();
                this.showStep(4);
                
                // Enable create video button
                document.getElementById('create-video-btn').disabled = false;
            } else {
                throw new Error(data.error || 'Failed to generate audio');
            }
        } catch (error) {
            console.error('Error generating audio:', error);
            alert('Error generating audio: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayAudio() {
        const container = document.getElementById('audio-container');
        
        container.innerHTML = `
            <div style="text-align: center; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                <h4>🎵 Narration Audio Generated</h4>
                <div class="audio-player" style="margin: 20px 0;">
                    <audio controls style="width: 100%; max-width: 600px;">
                        <source src="/view/${this.audioFile}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                <p style="color: #666; margin: 10px 0;">
                    <strong>Audio file:</strong> ${this.audioFile}
                </p>
                <p style="color: #666; font-size: 14px;">
                    🎧 Listen to your narration above, then create the final video!
                </p>
            </div>
        `;
    }
    
    async createVideo() {
        if (!this.audioFile || this.images.length === 0) {
            alert('Audio and images are required to create video.');
            return;
        }
        
        // Get successful image filenames
        const imageFiles = this.images
            .filter(img => !img.error && img.filename)
            .map(img => img.filename);
        
        if (imageFiles.length === 0) {
            alert('No valid images available for video creation.');
            return;
        }
        
        this.showLoading(true);
        
        try {
            const response = await fetch('/create-video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    image_files: imageFiles,
                    audio_file: this.audioFile
                })
            });
            
            const data = await response.json();
            
            if (data.success) {
                this.videoFile = data.video_filename;
                this.displayOutput();
                this.showStep(5);
            } else {
                throw new Error(data.error || 'Failed to create video');
            }
        } catch (error) {
            console.error('Error creating video:', error);
            alert('Error creating video: ' + error.message);
        } finally {
            this.showLoading(false);
        }
    }
    
    displayOutput() {
        const container = document.getElementById('output-container');
        
        const imageFiles = this.images
            .filter(img => !img.error && img.filename)
            .map(img => img.filename);
        
        const isHtml = this.videoFile && this.videoFile.endsWith('.html');
        const videoLabel = isHtml ? '📄 Download Slideshow (HTML)' : '🎬 Download Video (MP4)';
        
        container.innerHTML = `
            <div class="download-section">
                <h4>🎉 Your Teaching Content is Ready!</h4>
                
                <!-- Inline Video/Slideshow Display -->
                <div class="video-display" style="margin: 20px 0; padding: 20px; background: #f8f9fa; border-radius: 10px;">
                    ${isHtml ? 
                        `<h5>📺 Interactive Slideshow</h5>
                         <div style="border: 2px solid #ddd; border-radius: 8px; overflow: hidden;">
                             <iframe src="/view/${this.videoFile}" 
                                     width="100%" 
                                     height="600" 
                                     frameborder="0"
                                     style="display: block;">
                             </iframe>
                         </div>
                         <p style="margin-top: 10px; color: #666;">
                             <strong>Interactive Features:</strong> Auto-play, keyboard navigation (arrow keys), audio sync
                         </p>` :
                        `<h5>🎬 Teaching Video</h5>
                         <video controls style="width: 100%; max-width: 800px; border-radius: 8px;">
                             <source src="/view/${this.videoFile}" type="video/mp4">
                             Your browser does not support the video element.
                         </video>`
                    }
                </div>
                
                <!-- Audio Player -->
                <div class="audio-display" style="margin: 20px 0; padding: 15px; background: #e3f2fd; border-radius: 8px;">
                    <h5>🎵 Narration Audio</h5>
                    <audio controls style="width: 100%; max-width: 600px;">
                        <source src="/view/${this.audioFile}" type="audio/mpeg">
                        Your browser does not support the audio element.
                    </audio>
                </div>
                
                <!-- Image Gallery -->
                <div class="images-gallery" style="margin: 20px 0;">
                    <h5>🖼️ Generated Images</h5>
                    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px;">
                        ${imageFiles.map((filename, index) => 
                            `<div style="text-align: center; background: white; padding: 10px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                                <img src="/view/${filename}" 
                                     alt="Scene ${index + 1}" 
                                     style="width: 100%; height: 150px; object-fit: cover; border-radius: 6px; margin-bottom: 8px;">
                                <p style="margin: 0; font-size: 14px; color: #666;">Scene ${index + 1}</p>
                            </div>`
                        ).join('')}
                    </div>
                </div>
                
                <!-- Download Links -->
                <div class="download-links-section" style="margin-top: 30px; padding-top: 20px; border-top: 2px solid #eee;">
                    <h5>📥 Download Files</h5>
                    <div class="download-links">
                        <a href="/download/${this.videoFile}" class="download-link" download>
                            ${videoLabel}
                        </a>
                        <a href="/download/${this.audioFile}" class="download-link" download>
                            🎵 Download Audio (MP3)
                        </a>
                        ${imageFiles.map(filename => 
                            `<a href="/download/${filename}" class="download-link" download>
                                🖼️ ${filename}
                            </a>`
                        ).join('')}
                    </div>
                </div>
            </div>
        `;
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new TeachingVideoApp();
});