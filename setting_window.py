import tkinter
import customtkinter as ctk
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SettingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("490x470")
        self.bind("<FocusIn>", self.on_focus_in)  # Focus in on window once its open.
        self.grab_set()  # Prevent main window from being usable until this window is closed.
        self.title("Settings")
        self.resizable(False, False)

        # Create Frames
        self.create_main_frame()
        self.create_save_button()
        self.create_bot_sla_frame()
        self.create_home_delivery_frame()

        # Create Starting Widgets
        self.widgets = [
            {"label_text": "Number of Months Back", "entry_placeholder": "2", "default_value": "2"},
            {"label_text": "Number of Days Back", "entry_placeholder": "0", "default_value": "0"},
            {"label_text": "From Airport", "entry_placeholder": "WPG", "default_value": "WPG"},
            {"label_text": "To Airport", "entry_placeholder": "Please Select", "default_value": "Please Select"},
        ]

        # Insert Widgets on Setting Window
        self.insert_widgets(self.bot_sla_frame, self.create_bot_sla_widgets())
        self.insert_widgets(self.home_frame, self.create_home_delivery_widgets())


    def create_main_frame(self):
        """Main Setting Frame"""
        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.pack()

    def create_bot_sla_frame(self):
        """Bot/SLA Frame"""
        self.bot_sla_frame = ctk.CTkFrame(master=self.main_frame, height=380)
        self.bot_sla_frame.pack_propagate(False)
        self.bot_sla_frame.pack(side="left", padx=(0, 30), pady=(20, 0))

    def create_home_delivery_frame(self):
        """Home Delivery Frame"""
        self.home_frame = ctk.CTkFrame(master=self.main_frame, height=380)
        self.home_frame.pack_propagate(False)
        self.home_frame.pack(side="left", pady=(20, 0))

    def create_save_button(self):
        """Save Button"""
        save_button_frame = ctk.CTkFrame(master=self.main_frame, fg_color="transparent")
        save_button_frame.pack(side="bottom")

        self.save_button = ctk.CTkButton(master=save_button_frame, text="Save Settings", width=430)
        self.save_button.pack(pady="20")


    @classmethod
    def insert_widgets(cls, frame, widget_list):
        """Insert all the widgets on setting screen"""
        # Using enumerate to access the first item in the list, as that will be the header text.
        for index, field in enumerate(widget_list):
            if index == 0:
                header_label = ctk.CTkLabel(master=frame, text=field["label_text"], font=("Helvetica", 12,
                                                                                          "bold", "underline"))
                header_label.pack()
            else:
                label = ctk.CTkLabel(master=frame, text=field["label_text"])
                label.pack()

                entry = ctk.CTkEntry(master=frame, width=100, justify="center", placeholder_text=field["entry_placeholder"])
                entry.insert(ctk.END, field["default_value"])
                entry.pack()

    def create_bot_sla_widgets(self):
        """Add necessary widgets to the starting widget list"""
        sla_fields = [
            {"label_text": "Bot/SLA Report Settings"},
            {"label_text": "Days", "entry_placeholder": "8", "default_value": "8"},
            {"label_text": "Top Priority", "entry_placeholder": "-6", "default_value": "-6"}
        ]

        return sla_fields + self.widgets

    def create_home_delivery_widgets(self):
        """Add necessary widgets to the starting widget list and modify any values needed to be changed"""
        for widget in self.widgets:
            if widget['label_text'] == "Number of Months Back":
                widget["entry_placeholder"] = "0"
                widget["default_value"] = "0"
            elif widget["label_text"] == "Number of Days Back":
                widget["entry_placeholder"] = "2"
                widget["default_value"] = "2"

        # Insert Header Text.
        self.widgets.insert(0, {"label_text": "Home Delivery Settings"})
        self.widgets.append({"label_text": "Keyword", "entry_placeholder": "SYSCO", "default_value": "SYSCO"})

        return self.widgets

    def on_focus_in(self, event):
        """Bring setting window to the front when opened"""
        self.attributes("-topmost", True)
