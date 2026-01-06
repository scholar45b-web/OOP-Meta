import json
import os
from datetime import datetime

class UserStats:
    def __init__(self, filename="user_data.json"):
        self.filename = filename
        self.data = self._load_data()

    def _load_data(self):
        #Read file
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return [] # Corrupt file, return empty list
        return []

    def save_session(self, duration_seconds):
        #Write file
        if duration_seconds < 1: return # Don't save empty sessions

        entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "duration": int(duration_seconds),
            "score": int(duration_seconds * 10) # Simple gamification
        }
        self.data.append(entry)
        
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4)
    
    def get_total_time(self):
        """Returns total seconds focused across all history"""
        return sum(entry['duration'] for entry in self.data)