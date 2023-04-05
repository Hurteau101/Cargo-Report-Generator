import customtkinter as ctk


class PopUpWindow(ctk.CTkToplevel):
    def __init__(self, theme: str, title: str, size: str):
        super().__init__()
        self.geometry(size)
        self.title(title)
        ctk.set_appearance_mode(theme)
        self.bind("<FocusIn>", self.on_focus_in)  # Focus in on window once its open.
        self.grab_set()  # Prevent main window from being usable until this window is closed.
        self.resizable(False, False)

    def on_focus_in(self, event) -> None:
        """
        Bring the Window in front of the previous GUI Window.
        :param event: Required by the bind method call, but not used in the method body.
        """
        self.attributes("-topmost", True)
