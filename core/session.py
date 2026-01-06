from abc import ABC, abstractmethod
from core.timer import TimerEngine

class Session(ABC):
    def __init__(self, timer: TimerEngine):
        self.timer = timer
        self.can_flow = False
    
    @abstractmethod
    def start(self):
        """Every session must define how it starts."""
        pass

    def stop(self):
        """Common behavior for all sessions."""
        elapsed = self.timer.get_elapsed_time()
        self.timer.stop()
        return elapsed 

class FocusSession(Session):
    def __init__(self, timer: TimerEngine):
        super().__init__(timer)
        
        self.can_flow = True
    def start(self):
        print("Starting Focus Session: 25 Minutes")
        self.timer.start(25)

class RestSession(Session):
    def start(self):
        print("Starting Rest Session: 5 Minutes")
        self.can_flow = False 
        self.timer.start(5)


class SessionManager:
    def __init__(self, timer_component, user_stats=None):
        self.timer = timer_component
        self.user_stats = user_stats
        self.current_session = None 
    
    def start_focus(self):
        """Starts a Focus Session (25 mins, Flow allowed)"""
        self.current_session = FocusSession(self.timer)
        self.current_session.start()

    def start_rest(self, duration_minutes):
        """Starts a Rest Session (Fixed time, No Flow)"""
        self.current_session = RestSession(self.timer)
        self.timer.start(duration_minutes)


    def stop_session(self):
        """
        Called when the user clicks 'STOP'.
        """
        if not self.current_session:
            return {"work_time": 0, "rest_needed": 0}
        elapsed_seconds = self.current_session.stop()

        if isinstance(self.current_session, RestSession):
            suggested_rest_seconds = 0
            session_type = "Rest"
        else:
            suggested_rest_seconds = elapsed_seconds / 4
            session_type = "Focus"
        
        return {
            "work_time": elapsed_seconds,
            "rest_needed": suggested_rest_seconds,
            "type": session_type
        }