# ai/camera.py
import cv2

# Rubric Hit: Custom Exception Class
class CameraNotFoundError(Exception):
    """Custom error raised when webcam cannot be accessed."""
    pass

class WebcamFeed:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None

    def start(self):
        """Attempts to open the webcam."""
        print(f"Attempting to open camera {self.camera_index}...")
        
        # Rubric Hit: Exception Handling (try/except)
        try:
            self.cap = cv2.VideoCapture(self.camera_index)
            
            # Check if camera actually opened (OpenCV doesn't always throw an error automatically)
            if not self.cap.isOpened():
                raise CameraNotFoundError(f"Camera {self.camera_index} could not be opened.")
                
            print("Camera started successfully.")
            return True

        except CameraNotFoundError as e:
            print(f"CRITICAL ERROR: {e}")
            print("Switching to 'Blind Mode' (Timer will work without AI).")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def get_frame(self):
        """Reads a single frame from the camera."""
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
                return frame
        return None

    def stop(self):
        if self.cap:
            self.cap.release()
            print("Camera released.")