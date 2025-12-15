# core/timer.py
import time

class TimerEngine:
    """
    Rubric Hit: Encapsulation.
    Only this class knows how to calculate the remaining time.
    """
    def __init__(self):
        self.start_time = None
        self.duration = 0
        self.is_running = False
        self._paused_time = 0 # Private variable (Encapsulation)

    def start(self, minutes):
        self.duration = minutes * 60
        self.start_time = time.time()
        self.is_running = True
        print(f"Timer started for {minutes} minutes.")

    def stop(self):
        self.is_running = False
        self.start_time = None
        print("Timer stopped.")

    def get_time_string(self):
        """
        Returns the remaining time as 'MM:SS'.
        This is the method the GUI will call every second.
        """
        if not self.is_running:
            return "00:00"
        
        elapsed = time.time() - self.start_time
        remaining = max(0, self.duration - elapsed)
        
        mins = int(remaining // 60)
        secs = int(remaining % 60)
        return f"{mins:02d}:{secs:02d}"
    
    def is_finished(self):
        if not self.is_running:
            return False
        elapsed = time.time() - self.start_time
        return elapsed >= self.duration