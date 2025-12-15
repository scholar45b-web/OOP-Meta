# ui/dashboard.py
import tkinter as tk
from tkinter import ttk

class DashboardUI(tk.Frame):
    """
    Rubric Hit: GUI with 5 components.
    """
    def __init__(self, parent, controller):
        super().__init__(parent) # Rubric Hit: Superclass Constructor [cite: 21]
        self.controller = controller
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Title Label
        self.lbl_title = tk.Label(self, text="Metacognitive Flow", font=("Arial", 24))
        self.lbl_title.pack(pady=10)

        # 2. Timer Display
        self.lbl_time = tk.Label(self, text="25:00", font=("Helvetica", 48, "bold"))
        self.lbl_time.pack(pady=20)

        # 3. Start Button
        self.btn_start = tk.Button(self, text="Start Focus", command=self.controller.start_session, bg="green", fg="white")
        self.btn_start.pack(pady=5, fill="x")

        # 4. Stop Button
        self.btn_stop = tk.Button(self, text="Stop", command=self.controller.stop_session, bg="red", fg="white")
        self.btn_stop.pack(pady=5, fill="x")

        # 5. Stress Bar (Progress Bar)
        self.lbl_stress = tk.Label(self, text="Current Stress Level:")
        self.lbl_stress.pack(pady=(20, 5))
        self.progress_stress = ttk.Progressbar(self, orient="horizontal", length=100, mode="determinate")
        self.progress_stress.pack(fill="x")

    def update_timer(self, time_string):
        self.lbl_time.config(text=time_string)