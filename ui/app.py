# ui/app.py
import tkinter as tk
from ui.dashboard import DashboardUI
from core.timer import TimerEngine

# At the top of ui/app.py, add this import:
from core.session import FocusSession
# Third iteration after ai/camera.py is added
from ai.camera import WebcamFeed
from ai.sensor import EmotionSensor  # <--- THIS WAS MISSING OR BROKEN

class MetacognitiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flow Engine v1.0")
        self.geometry("400x500")
        
        # Initialize Hardware
        self.camera = WebcamFeed()
        self.camera.start() # This will try to open the cam

        # Initialize AI (The Brain) <--- ADD THIS BLOCK
        self.sensor = EmotionSensor()
        self.sensor.start()

        # Initialize components
        self.timer_logic = TimerEngine()
        self.ui = DashboardUI(self, self) # Pass 'self' as controller
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.update_clock()

        # Start the update loop
        self.update_clock()

    #def start_session(self):
        #print("UI: Start button clicked")
        #self.timer_logic.start(25) # Start 25 min timer
# ... inside the MetacognitiveApp class ...

    def start_session(self):
        print("UI: Start button clicked")
        
        # OLD CODE (Delete or comment out):
        # self.timer_logic.start(25)

        # NEW CODE (Object-Oriented):
        # We create a specific 'FocusSession' object.
        # This satisfies "Passing Objects" because we pass self.timer_logic into it.
        session = FocusSession(self.timer_logic)
        session.start()
        
    def stop_session(self):
        print("UI: Stop button clicked")
        self.timer_logic.stop()
        self.ui.update_timer("00:00")

    def update_clock(self):
        """
        The heartbeat of the app. Runs every 100ms.
        """
        # 1. ALWAYS update the AI stats (Even if timer is stopped)
        stress_val = self.sensor.stress_level
        emotion = self.sensor.current_emotion
        
        # Update the GUI components
        self.ui.progress_stress['value'] = stress_val
        self.ui.lbl_stress.config(text=f"Stress Level: {stress_val}% ({emotion})")

     # 2. Update Timer ONLY if running
        if self.timer_logic.is_running:
            time_str = self.timer_logic.get_time_string()
            self.ui.update_timer(time_str)
            
            if self.timer_logic.is_finished():
                self.timer_logic.stop()
                print("Session Complete!")
        
        # Schedule the next check
        self.after(100, self.update_clock)

    # Add this method inside MetacognitiveApp
    def on_close(self):
        print("Shutting down...")
        self.camera.stop()
        self.sensor.stop() # <--- STOP THE THREAD SAFELY
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.destroy()