import customtkinter as ctk
from datetime import datetime
from webpage_loader import CargoWebpage
from dotenv import load_dotenv
import os
import tkinter as tk


# Loading the environment variables into constants.
load_dotenv()
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("CARGO_URL")


class CargoInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        load_dotenv()
        self.title("Cargo Interface")
        self.geometry("500x350")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.resizable(False, False)

        # Main Frame Layout
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(expand=True, fill="both")

        # Tab Layout
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(expand=True, fill="both")
        self.tabview.add("SLA/Bot Report")
        self.tabview.add("Home Delivery")

        # SLA/Bot Report - Setting Frame
        self.setting_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"), height=40)
        self.setting_frame.pack(fill="x", pady=(10, 20))

        # SLA/Bot Report - Main Frame
        self.main_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"))
        self.main_frame.pack(fill="x", pady=(0, 10))

        # Settings
        self.setting_label = ctk.CTkLabel(master=self.setting_frame, text="Settings:")
        self.setting_label.pack()

        # Days Setting Frame
        self.day_frame = ctk.CTkFrame(master=self.setting_frame, height=40, fg_color="transparent")
        self.day_frame.pack(side="left", padx=(80, 50), pady=(0, 20))

        # Date Setting Frame
        self.date_frame = ctk.CTkFrame(master=self.setting_frame, height=40, fg_color="transparent")
        self.date_frame.pack(side="left", pady=(0, 20))

        # Day Settings
        self.day_label = ctk.CTkLabel(master=self.day_frame, text="Days")
        self.day_label.pack()

        self.day_box = ctk.CTkEntry(master=self.day_frame)
        self.day_box.pack()

        # Date Setting
        self.date_label = ctk.CTkLabel(master=self.date_frame, text="Date")
        self.date_label.pack()

        self.date_box = ctk.CTkEntry(master=self.date_frame)
        self.date_box.pack(side="left")

        # SLA/Bot Report - Main Layout
        self.button = ctk.CTkButton(master=self.main_frame, text="Webpage Load")
        self.button.grid(row=0, column=0)
        self.spin = tk.Spinbox(master=self.main_frame, from_=0, to=10, bd=3, justify="center", wrap=False)
        self.spin.grid(row=1, column=0, pady=10)

    def default_day_value(self):
        self.day_box.insert(ctk.END, "8")

    def default_date_value(self):
        today_date = datetime.today().date()
        self.date_box.insert(ctk.END, today_date.strftime("%d-%b-%Y"))

    def sla_bot_report_click(self):
        load_dotenv()
        self.cargo.load_url(os.getenv("CARGO_URL"))

cargo = CargoInterface()
cargo.mainloop()
