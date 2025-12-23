import tkinter as tk

class StatsUI(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#2c3e50")
        
        # 1. Title
        self.lbl_title = tk.Label(self, text="Session Complete!", 
                                font=("Arial", 24, "bold"), bg="#2c3e50", fg="#f1c40f")
        self.lbl_title.pack(pady=30)
        
        # 2. Total Time Display
        self.lbl_total = tk.Label(self, text="Total Focus Time: 0 mins", 
                                font=("Arial", 16), bg="#2c3e50", fg="white")
        self.lbl_total.pack(pady=10)

        # 3. History List (Leaderboard)
        self.lbl_history = tk.Label(self, text="Recent Sessions:", 
                                  font=("Arial", 12), bg="#2c3e50", fg="#bdc3c7")
        self.lbl_history.pack(pady=(20, 5))
        
        self.listbox = tk.Listbox(self, height=5, width=40, bg="#34495e", fg="white")
        self.listbox.pack(pady=5)

        # 4. Back/Exit Button
        self.btn_back = tk.Button(self, text="Back to Timer", 
                                command=lambda: controller.show_frame("DashboardUI"),
                                bg="#3498db", fg="white")
        self.btn_back.pack(pady=20)

    def update_stats(self):
        """Called whenever we show this page"""
        stats_manager = self.controller.stats_manager
        total_sec = stats_manager.get_total_time()
        
        # Update Total
        self.lbl_total.config(text=f"Total Focus Time: {int(total_sec // 60)} mins")
        
        # Update Listbox
        self.listbox.delete(0, tk.END)
        # Show last 5 sessions
        for entry in reversed(stats_manager.data[-5:]):
            mins = entry['duration'] // 60
            self.listbox.insert(tk.END, f"{entry['date']} - {mins} mins ({entry['score']} pts)")