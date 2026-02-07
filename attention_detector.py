import cv2
import time
import threading
import os

class AttentionDetector:
    def __init__(self):
        # Initial state
        self.last_face_time = time.time()
        self.status = "focused"
        self.running = False
        self.lock = threading.Lock()
        
        # Path to Haar Cascade - Use absolute path relative to this script
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.cascade_path = os.path.join(current_dir, "haarcascade_frontalface.xml")
        
        # Check if cascade file exists
        if not os.path.exists(self.cascade_path):
            print(f"Warning: {self.cascade_path} not found. Face detection will not work.")
            self.face_cascade = None
        else:
            self.face_cascade = cv2.CascadeClassifier(self.cascade_path)

    def start(self):
        """Start the detection thread"""
        if self.running:
            return
            
        if self.face_cascade is None:
            print("Cannot start detection: Cascade file missing.")
            return

        self.running = True
        self.thread = threading.Thread(target=self._detection_loop, daemon=True)
        self.thread.start()
        print("👁️ Attention detection started.")

    def stop(self):
        """Stop the detection thread"""
        self.running = False
        if hasattr(self, 'thread'):
            self.thread.join()
        print("👁️ Attention detection stopped.")

    def _detection_loop(self):
        """Background loop to read webcam and detect faces"""
        # Try multiple camera indices if 0 fails
        cap = None
        for index in [0, 1, 2]:
            print(f"Attempting to open camera index {index}...")
            temp_cap = cv2.VideoCapture(index)
            if temp_cap.isOpened():
                print(f"Successfully opened camera index {index}")
                cap = temp_cap
                break
            else:
                temp_cap.release()
        
        if cap is None:
            print("Error: Could not open any webcam (tried indices 0, 1, 2).")
            self.running = False
            return

        while self.running:
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.1)
                continue

            # Convert to grayscale for efficient detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )

            current_time = time.time()
            
            # Update state safely with lock
            with self.lock:
                if len(faces) > 0:
                    # Face found, reset timer
                    self.last_face_time = current_time
                    self.status = "focused"
                else:
                    # No face, check duration
                    elapsed = current_time - self.last_face_time
                    if elapsed > 8: # 8 second threshold
                        self.status = "distracted"
                    else:
                        self.status = "focused"
            
            # Small sleep to save CPU
            time.sleep(0.1)

        cap.release()

    def get_status(self):
        """Get the current attention status"""
        with self.lock:
            return self.status

# Create a global instance to be imported by app.py
detector = AttentionDetector()
