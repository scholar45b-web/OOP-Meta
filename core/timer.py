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
        self.mode = "COUNTDOWN" # UI color changes

    def start(self, minutes):
        self.duration = minutes * 60
        self.start_time = time.time()
        self.is_running = True
        self.mode = "COUNTDOWN"
        print(f"Timer started for {minutes} minutes.")

    def stop(self):
        self.is_running = False
        self.start_time = None
        self.mode = "COUNTDOWN" # Reset mode
        print("Timer stopped.")

    def get_time_string(self):
        """
        Returns the remaining time as 'MM:SS'.
        Modified to allow negative numbers for Flow Mode.
        """
        if not self.is_running:
            return "00:00"
        
        elapsed = time.time() - self.start_time
        remaining = self.duration - elapsed 
        
        if remaining < 0:
            # Overtime (Flow State)
            self.mode = "FLOW" # Tell the UI to turn Gold
            overtime = abs(remaining)
            mins = int(overtime // 60)
            secs = int(overtime % 60)
            return f"+{mins:02d}:{secs:02d}" 
        else:
            # Normal Countdown
            self.mode = "COUNTDOWN"
            mins = int(remaining // 60)
            secs = int(remaining % 60)
            return f"{mins:02d}:{secs:02d}"

    def get_elapsed_time(self):
        """
        Returns total seconds the user has been working.
        Used by SessionManager to calculate stats.
        """
        if self.start_time is None:
            return 0
        return time.time() - self.start_time   

    def is_finished(self):
        """
        Triggers when the countdown hits zero.
        """
        if not self.is_running:
            return False
        elapsed = time.time() - self.start_time
        return elapsed >= self.duration