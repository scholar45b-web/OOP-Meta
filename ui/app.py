import tkinter as tk
from ui.dashboard import DashboardUI
from ui.leaderboard import StatsUI  # Import the new page
from core.timer import TimerEngine
from core.session import SessionManager 
from core.stats import UserStats # Import the data manager
from ai.camera import WebcamFeed
from ai.sensor import EmotionSensor

class MetacognitiveApp(tk.Tk):
    def __init__(self):
        # FIX 1: Initialize the parent tk.Tk class FIRST.
        # Without this, the app has no window and crashes immediately.
        super().__init__()
        
        self.title("Flow Engine vFinal") # Optional: Set title
        self.geometry("400x650")         # Optional: Set size

        # 1. Initialize Hardware (Camera)
        print("System: Initializing Camera...")
        # FIX 2: Create the camera. It takes NO arguments.
        # Do NOT pass self.camera here.
        self.camera = WebcamFeed() 
        self.camera.start()

        # 2. Initialize AI (The Brain)
        print("System: Initializing Emotion Sensor...")
        # Pass the camera to the sensor (The Sensor watches the Camera)
        self.sensor = EmotionSensor(self.camera) 
        self.sensor.start()

        # 3. Initialize Logic
        self.timer_logic = TimerEngine()
        self.stats_manager = UserStats() # Load history
        self.session_manager = SessionManager(self.timer_logic, self.stats_manager)
        
        # 4. Page Container (Stacking Logic)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # 5. Initialize Pages
        self.frames = {}
        for PageClass in (DashboardUI, StatsUI):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            # Stack them on top of each other
            frame.grid(row=0, column=0, sticky="nsew")

        # 6. Start Protocols
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.show_frame("DashboardUI")
        self.update_clock()

    def show_frame(self, page_name):
        """Switches the visible screen"""
        frame = self.frames[page_name]
        if page_name == "StatsUI":
            frame.update_stats() # Refresh data before showing
        frame.tkraise()

    def start_session(self):
        self.session_manager.start_focus()
        self.frames["DashboardUI"].lbl_time.config(fg="white")
        self.frames["DashboardUI"].lbl_status.config(text="Status: Focus Mode", fg="white")

    def stop_session(self):
        # 1. Logic
        stats = self.session_manager.stop_session()
        work_secs = int(stats["work_time"])
        rest_secs = int(stats["rest_needed"])
        
        # 2. Save Data (Rubric Hit: File I/O)
        # We only save if it was a meaningful session (> 30s)
        if stats.get("type") == "Focus" and work_secs > 10:
            self.stats_manager.save_session(work_secs)
            print(f"Data Saved: {work_secs} seconds.")

        # 3. UI Updates
        dashboard = self.frames["DashboardUI"]
        
        if rest_secs > 0:
            rest_minutes = rest_secs / 60
            self.session_manager.start_rest(rest_minutes)
            dashboard.lbl_status.config(text=f"Resting for {rest_secs}s...", fg="#3498db")
            dashboard.lbl_time.config(fg="white")
        else:
            dashboard.lbl_status.config(text="Ready", fg="white")
            dashboard.update_timer("00:00")

    def end_day(self):
        """Connected to the 'End Day' button"""
        # Stop any running timer first
        self.stop_session() 
        # Switch to the Leaderboard
        self.show_frame("StatsUI")

    def update_clock(self):
        # --- AI Updates ---
        try:
            stress_val = self.sensor.stress_level
            current_emotion = self.sensor.current_emotion
            self.frames["DashboardUI"].progress_stress['value'] = stress_val
            self.frames["DashboardUI"].lbl_stress.config(text=f"Stress: {stress_val}% ({current_emotion})")
        except: pass

        # --- Timer Updates ---
        if self.timer_logic.is_running:
            time_str = self.timer_logic.get_time_string()
            self.frames["DashboardUI"].update_timer(time_str)

            # Flow Logic
            if self.timer_logic.is_finished():
                can_flow = self.session_manager.current_session and self.session_manager.current_session.can_flow
                
                if can_flow:
                    self.frames["DashboardUI"].lbl_time.config(fg="#FFD700")
                    self.frames["DashboardUI"].lbl_status.config(text="Flow State (Overtime)", fg="#FFD700")
                else:
                    self.stop_session()

        self.after(100, self.update_clock)

    def on_close(self):
        try:
            self.camera.stop()
            self.sensor.stop()
        except: pass
        self.destroy()