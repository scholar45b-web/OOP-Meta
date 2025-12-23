import tkinter as tk
from tkinter import ttk

class DashboardUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Set background color to match the modern look (dark blue-grey)
        self.configure(bg="#2c3e50") 
        self.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.create_widgets()

    def create_widgets(self):
        # 1. Title Label
        self.lbl_title = tk.Label(self, text="Metacognitive Flow", 
                                font=("Arial", 24), bg="#2c3e50", fg="white")
        self.lbl_title.pack(pady=10)

        # 2. Timer Display
        self.lbl_time = tk.Label(self, text="00:00", 
                               font=("Helvetica", 48, "bold"), bg="#2c3e50", fg="white")
        self.lbl_time.pack(pady=20)

        # --- NEW COMPONENT: STATUS LABEL ---
        # This was missing! It shows "Flow State", "Focus Mode", etc.
        self.lbl_status = tk.Label(self, text="Status: Ready", 
                                 font=("Arial", 12, "italic"), bg="#2c3e50", fg="#bdc3c7")
        self.lbl_status.pack(pady=5)
        # -----------------------------------

        # 3. Start Button
        self.btn_start = tk.Button(self, text="Start Focus", 
                                 command=self.controller.start_session, 
                                 bg="#27ae60", fg="white", font=("Arial", 12, "bold"))
        self.btn_start.pack(pady=5, fill="x")

        # 4. Stop Button
        self.btn_stop = tk.Button(self, text="Stop", 
                                command=self.controller.stop_session, 
                                bg="#c0392b", fg="white", font=("Arial", 12, "bold"))
        self.btn_stop.pack(pady=5, fill="x")

        # --- NEW BUTTON: END DAY ---
        self.btn_end = tk.Button(self, text="End Day & View Stats", 
                               command=self.controller.end_day, 
                               bg="#8e44ad", fg="white", font=("Arial", 10, "bold"))
        self.btn_end.pack(pady=20, fill="x")
        # ---------------------------

        # 5. Stress Display
        self.lbl_stress = tk.Label(self, text="Stress: 0% (Neutral)", 
                                 bg="#2c3e50", fg="white")
        self.lbl_stress.pack(pady=(20, 5))
        
        self.progress_stress = ttk.Progressbar(self, 
                                             orient="horizontal", length=100, mode="determinate")
        self.progress_stress.pack(fill="x")

    def update_timer(self, time_string):
        self.lbl_time.config(text=time_string)