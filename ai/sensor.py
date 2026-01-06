import cv2
import threading
import time
from deepface import DeepFace
from collections import deque

class EmotionSensor:
    def __init__(self, camera_feed):
        self.camera = camera_feed 
        
        self.current_emotion = "Neutral"
        self.is_running = False
        self.stress_level = 0
        self.emotion_buffer = deque(maxlen=5)

    def start(self):
        if not self.is_running:
            self.is_running = True
            thread = threading.Thread(target=self._sensing_loop)
            thread.daemon = True
            thread.start()
            print("AI: Emotion Sensor Started")

    def stop(self):
        self.is_running = False

    def _preprocess_frame(self, frame):
        # Digital Night Vision (CLAHE)
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)
        limg = cv2.merge((cl,a,b))
        return cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    def _sensing_loop(self):
        while self.is_running:
            # Borrow frame from Shared Camera
            raw_frame = self.camera.get_frame()
            
            if raw_frame is None:
                time.sleep(0.5)
                continue

            # Apply Filter
            frame = self._preprocess_frame(raw_frame)

            try:
                # Enforce detection to avoid analyzing walls
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True)
                emotions = result[0]['emotion'] 
                
                # SENSITIVITY PATCH: Check for smile trace > 50%
                if emotions['happy'] > 50.0:
                    raw_emotion = 'happy'
                else:
                    raw_emotion = result[0]['dominant_emotion']
                    # Filter weak negatives
                    score = emotions[raw_emotion]
                    if raw_emotion in ['fear', 'sad', 'angry'] and score < 50:
                        raw_emotion = 'neutral'

                self.emotion_buffer.append(raw_emotion)
                if len(self.emotion_buffer) > 0:
                    smoothed = max(set(self.emotion_buffer), key=self.emotion_buffer.count)
                else:
                    smoothed = raw_emotion

                self.current_emotion = smoothed
                self._calculate_stress(smoothed)
                
            except Exception:
                self.current_emotion = "No Face"
                self._decay_stress()
            
            time.sleep(2) 

    def _calculate_stress(self, emotion):
        high_stress = ['sad', 'fear', 'angry', 'disgust']
        relax_triggers = ['happy', 'neutral']
        
        if emotion in high_stress:
            self.stress_level += 5
        elif emotion in relax_triggers:
            self.stress_level -= 2
            
        self.stress_level = max(0, min(100, self.stress_level))

    def _decay_stress(self):
        if self.stress_level > 0:
            self.stress_level -= 5 
        self.stress_level = max(0, self.stress_level)
        
    @property
    def stress_level_val(self):
        return self.stress_level