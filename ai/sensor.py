import threading
import time
import cv2  # <--- CRITICAL FIX 1: Missing Import
from deepface import DeepFace 

class SensorDataError(Exception):
    """Raised when the sensor produces invalid readings."""
    pass

class EmotionSensor:
    def __init__(self):
        self.running = False
        self.current_emotion = "Neutral"
        self.stress_level = 0
        
        # <--- CRITICAL FIX 2: Initialize the Camera
        # 0 is the default webcam ID.
        self.cap = cv2.VideoCapture(0) 

        # <--- CRITICAL FIX 3: Point to the REAL AI Loop (_sensing_loop), not the fake one
        self.thread = threading.Thread(target=self._sensing_loop)
        self.thread.daemon = True 
    
    def _sensing_loop(self):
        # <--- CRITICAL FIX 4: Use 'self.running' consistently
        while self.running: 
            ret, frame = self.cap.read()
            if not ret:
                continue

            try:
                # DeepFace Analysis
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                
                dominant_emotion = result[0]['dominant_emotion']
                self.current_emotion = dominant_emotion
                
                self._calculate_stress(dominant_emotion)
                
            except Exception as e:
                print(f"DeepFace Error: {e}")
            
            # Sleep to save CPU (DeepFace is heavy)
            time.sleep(2) 

    def _calculate_stress(self, emotion):
        """Helper to map emotion strings to stress numbers"""
        high_stress = ['sad', 'fear', 'angry', 'disgust']
        
        if emotion in high_stress:
            self.stress_level += 10
        elif emotion == 'happy':
            self.stress_level = max(0, self.stress_level - 5)
            
        # Safety Clamp
        self.stress_level = max(0, min(100, self.stress_level))

    def get_stress_data(self):
        return self.stress_level, self.current_emotion

    def start(self):
        if not self.running:
            self.running = True
            self.thread.start()
            print("AI: Emotion Sensor Thread Started.")

    def stop(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release() # Release camera hardware
        print("AI: Stopping Sensor...")