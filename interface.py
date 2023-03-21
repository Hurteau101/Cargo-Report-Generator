import customtkinter as ctk
from webpage_loader import CargoWebpage
from dotenv import load_dotenv
import os
import tkinter as tk
import tkinter.messagebox as messagebox
import threading
from setting_window import SettingWindow


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
        self.setting_window = None

        # Main Frame Layout
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(expand=True, fill="both")

        # Menu Bar
        file_menu = tk.Menu(master=self)
        submenu = tk.Menu(file_menu, tearoff=0)
        submenu.add_command(label="Settings", command=self.open_settings)
        file_menu.add_cascade(label="File", menu=submenu)
        self.config(menu=file_menu)

        # Tab Layout
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(expand=True, fill="both")
        self.tabview.add("SLA/Bot Report")
        self.tabview.add("Home Delivery")

        # SLA/Bot Report - Main Frame
        self.main_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"))
        self.main_frame.pack(fill="x", pady=(0, 10))

        # SLA/Bot Report - Main Layout
        self.button = ctk.CTkButton(master=self.main_frame, text="Webpage Load", command=self.sla_bot_report_command)
        self.button.pack()


    def _set_credentials(self):
        self.webpage.username = USERNAME
        self.webpage.password = PASSWORD

    def start_selenium(self):
        self.webpage.start_selenium()
        self.webpage.load_url(URL)

    @classmethod
    def display_error(cls, title, message):
        messagebox.showerror(cls, message)

    def check_page_load(self):
        """Check if the webpage is loaded correctly"""
        # Check if starting webpage is loaded correctly. If it's not add a popup.
        if not self.webpage.check_webpage_loaded("//input[@id='UserName']", wait_time=5):
            messagebox.showerror("Webpage Load Error", "The webpage did not load correctly")
            return False
        return True

    def login_success(self):
        """Check if login was successful. Similar to check_login on webpage_loader class, this is to check if a popup
        is needed if login was unsuccessful"""
        # If login was unsuccessful provide popup.
        if not self.webpage.check_login():
            messagebox.showerror("Login Unsuccessful", "The login was unsuccessful")
            return False
        return True

    def sla_bot_report_command(self):
        thread = threading.Thread(target=self.sla_bot_report_click)
        thread.start()

    def sla_bot_report_click(self):
        self.start_selenium()
        self._set_credentials()

        # Check all conditions. This will make sure nothing failed before making it to the "Airway bills to Ship Report"
        loading_waybill_page = all((self.check_page_load(),
                                    self.webpage.login(),
                                    self.login_success(),
                                    self.webpage.waybills_to_ship_page()))

        if loading_waybill_page:
            pass

    def open_settings(self):
        if self.setting_window is None or not self.setting_window.winfo_exists():
            self.setting_window = SettingWindow()

        else:
            self.setting_window.focus()


cargo = CargoInterface()
cargo.mainloop()



