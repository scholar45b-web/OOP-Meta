import cv2
from PIL import Image, ImageTk
import threading

class WebcamFeed:
    def __init__(self):
        # Initialize Camera
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.is_running = False
        self.current_image = None # For UI
        self.last_frame = None    # For AI (Raw Data)
        self.lock = threading.Lock() # Thread safety

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._update_loop)
            self.thread.daemon = True
            self.thread.start()

    def stop(self):
        self.is_running = False
        if self.cap.isOpened():
            self.cap.release()

    def _update_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                with self.lock:
                    # 1. Save Raw Frame for AI
                    self.last_frame = frame.copy() 
                    
                    # 2. Convert for UI (BGR -> RGB)
                    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                    img = Image.fromarray(cv2image)
                    self.current_image = ImageTk.PhotoImage(image=img)

    def get_frame(self):
        """Called by EmotionSensor to borrow the latest image"""
        with self.lock:
            return self.last_frame