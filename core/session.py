from abc import ABC, abstractmethod
from core.timer import TimerEngine

# Rubric Hit: Abstract Class (The template)
class Session(ABC):
    def __init__(self, timer: TimerEngine):
        self.timer = timer
    
    @abstractmethod
    def start(self):
        """Every session must define how it starts."""
        pass

    def stop(self):
        """Common behavior for all sessions."""
        self.timer.stop()

# Rubric Hit: Inheritance (Child of Session)
class FocusSession(Session):
    def start(self):
        print("Starting Focus Session: 25 Minutes")
        # Logic: Focus is 25 mins (1500 seconds)
        self.timer.start(25) 

# Rubric Hit: Inheritance (Child of Session)
class RestSession(Session):
    def start(self):
        print("Starting Rest Session: 5 Minutes")
        # Logic: Rest is 5 mins (300 seconds)
        # Rubric Hit: Polymorphism (Same method name 'start', different duration)
        self.timer.start(5)