import customtkinter as ctk


class SettingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("400x300")
        self.bind("<FocusIn>", self.on_focus_in)
        self.grab_set() # Prevent main window from being usable until this window is closed.

    def on_focus_in(self, event):
        """Bring setting window to the front when opened"""
        self.attributes("-topmost", True)
