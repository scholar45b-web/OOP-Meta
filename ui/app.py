# ui/app.py
import tkinter as tk
from ui.dashboard import DashboardUI
from core.timer import TimerEngine

class MetacognitiveApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Flow Engine v1.0")
        self.geometry("400x500")
        
        # Initialize components
        self.timer_logic = TimerEngine()
        self.ui = DashboardUI(self, self) # Pass 'self' as controller

        # Start the update loop
        self.update_clock()

    def start_session(self):
        print("UI: Start button clicked")
        self.timer_logic.start(25) # Start 25 min timer

    def stop_session(self):
        print("UI: Stop button clicked")
        self.timer_logic.stop()
        self.ui.update_timer("00:00")

    def update_clock(self):
        """
        The heartbeat of the app. Runs every 100ms.
        """
        if self.timer_logic.is_running:
            # Get the math from the engine
            time_str = self.timer_logic.get_time_string()
            # Send it to the UI
            self.ui.update_timer(time_str)
            
            if self.timer_logic.is_finished():
                self.timer_logic.stop()
                print("Session Complete!")
        
        # Schedule the next check in 100ms
        self.after(100, self.update_clock)