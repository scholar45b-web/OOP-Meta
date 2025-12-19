import cv2
import threading
import time
from deepface import DeepFace

class EmotionSensorService:
    def __init__(self):
        self.cap = cv2.VideoCapture(0) # 0 is usually the default camera
        self.current_emotion = "Neutral"
        self.is_running = False
        self.stress_level = 0
        
    def start_sensing(self):
        self.is_running = True
        # Run the heavy loop in a separate background thread
        sensing_thread = threading.Thread(target=self._sensing_loop)
        sensing_thread.daemon = True # Kills thread when app closes
        sensing_thread.start()

    def _sensing_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # Optimization: Only analyze every 50th frame or every 3 seconds
            # DeepFace is slow!
            try:
                # [Requirement: External Library Integration]
                # actions=['emotion'] analyzes the face for emotions
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
                
                # result is a list of dicts. Get the first face found.
                dominant_emotion = result[0]['dominant_emotion']
                self.current_emotion = dominant_emotion
                
                self._calculate_stress(dominant_emotion)
                
            except Exception as e:
                # [Requirement: Exception Handling]
                print(f"DeepFace Error: {e}")
            
            time.sleep(2) # Pause to save CPU

    def _calculate_stress(self, emotion):
        # Map emotions to stress (Logic)
        # tired/sad/fear = High Stress
        high_stress_triggers = ['sad', 'fear', 'angry', 'disgust']
        
        if emotion in high_stress_triggers:
            self.stress_level += 10
        elif emotion == 'happy':
            self.stress_level = max(0, self.stress_level - 5)
            
        # "Safety reset" logic you asked about earlier
        if self.stress_level > 100:
            self.stress_level = 100

    def get_stress_data(self):
        return self.stress_level, self.current_emotion

    def stop_sensing(self):
        self.is_running = False
        self.cap.release()