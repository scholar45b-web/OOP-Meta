import cv2
import threading
import time
from deepface import DeepFace
from collections import deque

class EmotionSensor: # Renamed to match your App import
    def __init__(self, camera_feed):
        # FIX 1: Receive the Shared Camera (No cv2.VideoCapture here!)
        self.camera = camera_feed 
        
        self.current_emotion = "Neutral"
        self.is_running = False
        self.stress_level = 0
        
        # Buffer to smooth out noise (last 5 frames)
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
        """
        Applies 'Digital Night Vision' (CLAHE) to see faces in dark rooms.
        """
        # Convert to LAB to isolate Lightness channel
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)

        # Apply CLAHE to Lightness channel only
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
        cl = clahe.apply(l)

        # Merge back
        limg = cv2.merge((cl,a,b))
        final = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)
        
        return final

    def _sensing_loop(self):
        while self.is_running:
            # FIX 2: Get frame from the Shared Camera
            raw_frame = self.camera.get_frame()
            
            if raw_frame is None:
                time.sleep(0.5)
                continue

            # FIX 3: Apply Digital Night Vision
            frame = self._preprocess_frame(raw_frame)

            try:
                # 1. Analyze with Enforced Detection (Prevents analyzing walls)
                result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=True)
                
                # Get specific emotion scores
                emotions = result[0]['emotion'] 
                
                # --- SENSITIVITY PATCH ---
                # If 'Happy' is even slightly visible (> 1%), count it as a smile.
                # This compensates for bad lighting.
                if emotions['happy'] > 1.0:
                    raw_emotion = 'happy'
                    # Optional Debug:
                    # print(f"AI: Trace Smile Detected ({emotions['happy']:.1f}%)")
                else:
                    # Otherwise, use the dominant one
                    raw_emotion = result[0]['dominant_emotion']
                    
                    # Logic Filter: Ignore weak negative emotions (shadows)
                    score = emotions[raw_emotion]
                    if raw_emotion in ['fear', 'sad', 'angry'] and score < 50:
                        raw_emotion = 'neutral'
                # -------------------------

                # Buffer Smoothing
                self.emotion_buffer.append(raw_emotion)
                if len(self.emotion_buffer) > 0:
                    smoothed = max(set(self.emotion_buffer), key=self.emotion_buffer.count)
                else:
                    smoothed = raw_emotion

                self.current_emotion = smoothed
                self._calculate_stress(smoothed)
                
            except Exception:
                # No face found -> User took a break
                self.current_emotion = "No Face"
                self._decay_stress()
            
            # Pause to save CPU
            time.sleep(2) 

    def _calculate_stress(self, emotion):
        """
        Updates stress level. 
        Note: 'Neutral' also lowers stress now.
        """
        high_stress = ['sad', 'fear', 'angry', 'disgust']
        relax_triggers = ['happy', 'neutral']
        
        if emotion in high_stress:
            self.stress_level += 5
        elif emotion in relax_triggers:
            self.stress_level -= 2
            
        # Keep within bounds (0-