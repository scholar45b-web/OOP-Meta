from abc import ABC, abstractmethod
from core.timer import TimerEngine

# Rubric Hit: Abstract Class (The template)
class Session(ABC):
    def __init__(self, timer: TimerEngine):
        self.timer = timer
        # CHANGE 1: Default behavior. Most sessions (like Rest) cannot flow.
        self.can_flow = False
    
    @abstractmethod
    def start(self):
        """Every session must define how it starts."""
        pass

    def stop(self):
        """Common behavior for all sessions."""
        # 1. Capture the data while the timer is still 'alive'
        elapsed = self.timer.get_elapsed_time()
        self.timer.stop()
        return elapsed # Calls the new method in TimerEngine

# Rubric Hit: Inheritance (Child of Session)
class FocusSession(Session):
    def __init__(self, timer: TimerEngine):
        super().__init__(timer)
        # CHANGE 3: Focus sessions ALLOW negative numbers (Flow Mode)
        # The Controller will check this flag before deciding to stop the timer.
        self.can_flow = True
    def start(self):
        print("Starting Focus Session: 25 Minutes")
        # Logic: Focus is 25 mins (1500 seconds)
        self.timer.start(1)

# Rubric Hit: Inheritance (Child of Session)
class RestSession(Session):
    def start(self):
        print("Starting Rest Session: 5 Minutes")
        # Logic: Rest is 5 mins (300 seconds)
        # Rubric Hit: Polymorphism (Same method name 'start', different duration)
        self.can_flow = False # Rest sessions must stop exactly at 00:00
        self.timer.start(5)

# core/session.py

class SessionManager:
    def __init__(self, timer_component, user_stats=None):
        self.timer = timer_component
        self.user_stats = user_stats
        self.current_session = None # Tracks if we are in Focus or Rest
    
    def start_focus(self):
        """Starts a Focus Session (25 mins, Flow allowed)"""
        self.current_session = FocusSession(self.timer)
        self.current_session.start()

    def start_rest(self, duration_minutes):
        """Starts a Rest Session (Fixed time, No Flow)"""
        self.current_session = RestSession(self.timer)
        # We manually override the timer for the calculated rest time
        self.timer.start(duration_minutes)


    def stop_session(self):
        """
        Called when the user clicks 'STOP'.
        """
        # Safety check
        if not self.current_session:
            return {"work_time": 0, "rest_needed": 0}

        # 1. Stop and get time
        elapsed_seconds = self.current_session.stop()
        
        # 2. Check Session Type (The Fix)
        # We check if the session we just finished was a REST session.
        if isinstance(self.current_session, RestSession):
            # If we just finished resting, we don't need MORE rest.
            suggested_rest_seconds = 0
            session_type = "Rest"
        else:
            # If we were Focusing, calculate the 1:4 rule.
            suggested_rest_seconds = elapsed_seconds / 4
            session_type = "Focus"
        
        return {
            "work_time": elapsed_seconds,
            "rest_needed": suggested_rest_seconds,
            "type": session_type
        }