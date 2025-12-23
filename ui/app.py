import tkinter as tk
from ui.dashboard import DashboardUI
from core.timer import TimerEngine
from core.session import SessionManager 
from ai.camera import WebcamFeed
from ai.sensor import EmotionSensor

class MetacognitiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flow Engine v2.0")
        self.geometry("400x600")
        
        # 1. Initialize Hardware (Camera)
        print("System: Initializing Camera...")
        self.camera = WebcamFeed()
        self.camera.start()

        # 2. Initialize AI (The Brain)
        print("System: Initializing Emotion Sensor...")
        self.sensor = EmotionSensor()
        self.sensor.start()

        # 3. Initialize Logic (Timer & Session)
        self.timer_logic = TimerEngine()
        self.session_manager = SessionManager(self.timer_logic)
        
        # 4. Initialize View (GUI)
        # We pass 'self' as the controller so Dashboard can call our methods
        self.ui = DashboardUI(self, self)
        
        # 5. Safety Protocols
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # 6. Start the Heartbeat
        self.update_clock()

    def start_session(self):
        """Connected to the 'START' button"""
        print("UI: Start button clicked")
        self.session_manager.start_focus()
        # Visual feedback: Change color to Focus Blue
        self.ui.lbl_time.config(fg="white")
        self.ui.lbl_status.config(text="Status: Focus Mode", fg="white")
        
    def stop_session(self):
        """Connected to the 'STOP' button"""
        print("UI: Stop button clicked")
        
        # 1. Ask Manager to stop and calculate stats
        stats = self.session_manager.stop_session()
        
        # 2. Extract the data
        work_secs = int(stats["work_time"])
        rest_secs = int(stats["rest_needed"])
        
        # 3. Visual Feedback
        print(f"Session Ended. Work: {work_secs}s. Rest: {rest_secs}s.")
        
        if rest_secs > 0:
            # --- AUTO-START REST TIMER ---
            # Convert seconds back to minutes for the timer engine
            rest_minutes = rest_secs / 60
            
            # Trigger the Rest Session
            self.session_manager.start_rest(rest_minutes)
            
            # Update UI
            self.ui.lbl_status.config(text=f"Resting for {rest_secs}s...", fg="#3498db")
            self.ui.lbl_time.config(fg="white") # Reset color from Gold
            
        else:
            # If they didn't work at all (0 seconds), just reset
            self.ui.lbl_status.config(text="Session Cancelled", fg="white")
            self.ui.update_timer("00:00")

    def update_clock(self):
        """
        The Master Loop (Running every 100ms).
        Handles: Time Updates, AI Polling, and Flow Logic.
        """
        
        # --- PART 1: AI & SENSOR DATA ---
        try:
            stress_val = self.sensor.stress_level
            current_emotion = self.sensor.current_emotion
            
            # Update the visual bars
            self.ui.progress_stress['value'] = stress_val
            self.ui.lbl_stress.config(text=f"Stress: {stress_val}% ({current_emotion})")
        except Exception:
            # If sensor isn't ready, don't crash the GUI
            current_emotion = "Neutral"
            stress_val = 0

        # --- PART 2: TIMER & FLOW LOGIC ---
        if self.timer_logic.is_running:
            # Update the countdown text
            time_str = self.timer_logic.get_time_string()
            self.ui.update_timer(time_str)

            # A. The Passive Advisor (Does NOT stop timer)
            if current_emotion in ["Fear", "Sad", "Angry"] and stress_val > 50:
                self.ui.lbl_status.config(text="High Stress Detected. Deep Breath?", fg="#e74c3c")
            elif self.timer_logic.mode == "FLOW": 
                self.ui.lbl_status.config(text="Flow State Active (Overtime)", fg="#f1c40f")

            # B. The Active Trigger (Flow vs Stop)
            if self.timer_logic.is_finished():
                
                # Check polymorphism: Can this session flow?
                can_flow = False
                if self.session_manager.current_session:
                    can_flow = self.session_manager.current_session.can_flow
                
                if can_flow:
                    # STAY IN FLOW: Turn text Gold
                    self.ui.lbl_time.config(fg="#FFD700") 
                else:
                    # STOP: Rest session is over.
                    self.stop_session()
                    print("Timer Finished (Rest Over).")
                    self.ui.lbl_status.config(text="Break Over! Back to Work.", fg="white")
        
        # Recursive call to keep loop alive
        self.after(100, self.update_clock)

    def on_close(self):
        """Clean shutdown of hardware threads."""
        print("System: Shutting down...")
        try:
            if hasattr(self, 'camera'): self.camera.stop()
            if hasattr(self, 'sensor'): self.sensor.stop()
        except Exception as e:
            print(f"Error checking hardware: {e}")
        
        self.destroy()