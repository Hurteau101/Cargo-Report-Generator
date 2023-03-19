import customtkinter as ctk
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from webpage_loader import CargoWebpage
from dotenv import load_dotenv
import os
import tkinter as tk


# Loading the environment variables into constants.
load_dotenv()
USERNAME = os.getenv("USERNAME_1")
PASSWORD = os.getenv("PASSWORD")
URL = os.getenv("CARGO_URL")


class CargoInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.webpage = CargoWebpage()
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
        self.day_frame.pack(side="left", padx=(120, 50), pady=(0, 20))

        # Date Setting Frame
        self.date_frame = ctk.CTkFrame(master=self.setting_frame, height=40, fg_color="transparent")
        self.date_frame.pack(side="left", pady=(0, 20))

        # Day Settings
        self.day_label = ctk.CTkLabel(master=self.day_frame, text="Days")
        self.day_label.pack()

        self.day_box = ctk.CTkEntry(master=self.day_frame, width=100, justify="center", placeholder_text="8")
        self.day_box.pack()
        self.default_day_value()

        # Date Setting
        self.date_label = ctk.CTkLabel(master=self.date_frame, text="Date")
        self.date_label.pack()

        self.date_box = ctk.CTkEntry(master=self.date_frame, width=100, justify="center",
                                     placeholder_text="19-Mar-2023")
        self.date_box.pack(side="left")
        self.default_date_value()

        # SLA/Bot Report - Main Layout
        self.button = ctk.CTkButton(master=self.main_frame, text="Webpage Load", command=self.sla_bot_report_click)
        self.button.pack()


    def default_day_value(self):
        self.day_box.insert(ctk.END, "8")

    def default_date_value(self):
        """Set default date. The default date is set 2 months from current date"""
        default_date = datetime.today().date() - relativedelta(months=2)
        self.date_box.insert(ctk.END, default_date.strftime("%d-%b-%Y"))

    def _set_credentials(self):
        self.webpage.username = USERNAME
        self.webpage.password = PASSWORD

    def _start_selenium(self):
        self.webpage.start_selenium()
        self.webpage.load_url(URL)

    def check_login(self):
        if not self.webpage.login():
            pass
            # TODO: Add popup to let user know unsucessful login

    def sla_bot_report_click(self):
        self._start_selenium()
        self._set_credentials()
        self.check_login()



cargo = CargoInterface()
cargo.mainloop()
