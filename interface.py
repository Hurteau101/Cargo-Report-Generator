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
        self.geometry("500x500")
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

        # Main Frame
        self.main_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"), fg_color="transparent")
        self.main_frame.pack()
        # self.main_frame.pack(fill="x", pady=(0, 10))

        # SLA/Bot Report Frame
        self.bot_sla_frame = ctk.CTkFrame(master=self.main_frame, height=380)
        self.bot_sla_frame.pack_propagate(False)
        self.bot_sla_frame.pack(side="left", pady=(20, 0), padx=(0, 30))

        # Option Frame
        self.option_frame = ctk.CTkFrame(master=self.main_frame, height=380)
        self.option_frame.pack_propagate(False)
        self.option_frame.pack(side="left", pady=(20, 0))

        # SLA/BOT Report Layout
        self.textbox = ctk.CTkTextbox(master=self.bot_sla_frame)
        self.textbox.pack()

        self.webpage_btn = ctk.CTkButton(master=self.bot_sla_frame, text="Webpage Loader",
                                         command=self.sla_bot_report_command)
        self.webpage_btn.pack(fill="x", pady="15")

        # Option Layout
        self.option_label = ctk.CTkLabel(master=self.option_frame, text="Options", font=("Helvetica", 12,
                                                                                         "bold", "underline"))
        self.option_label.pack()

        self.hide_text_cb = ctk.CTkCheckBox(master=self.option_frame, text="Hide Text", command=self.hide_textbox)
        self.hide_text_cb.pack(pady="5")

        self.script_running = ctk.StringVar(value="off")

        self.script_switch = ctk.CTkSwitch(master=self.option_frame, text="Script Running",
                                           command=self.stop_script_command, variable=self.script_running, onvalue="on",
                                           offvalue="off", state=ctk.DISABLED)
        self.script_switch.pack()

    def stop_script(self):
        """Stop selenium script, set swtich to off and disable switch"""
        self.set_script_switch("false")
        self.webpage.quit_selenium()

    def stop_script_command(self):
        """Create new thread for stopping selenium"""
        thread = threading.Thread(target=self.stop_script)
        thread.start()

    def set_script_switch(self, script_on: bool):
        """Set Script Switch Widget to on or off. True = on | False = off"""
        if not isinstance(script_on, bool):
            self.webpage.quit_selenium()
            raise TypeError(f"Expected 'script_on' to be of type 'bool' but got '{type(script_on)}' instead")

        if script_on:
            self.script_running = ctk.StringVar(value="on")
            self.script_switch.configure(state=ctk.NORMAL, variable=self.script_running)
        else:
            self.script_running = ctk.StringVar(value="off")
            self.script_switch.configure(state=ctk.DISABLED, variable=self.script_running)

    def sla_bot_report_command(self):
        """Create new thread for starting webscraper"""
        thread = threading.Thread(target=self.sla_bot_report_click)
        thread.start()

    def sla_bot_report_click(self):
        # Set switch value to on and enable switch.
        self.set_script_switch(True)

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

    def hide_textbox(self):
        checkbox_state = self.hide_text_cb.get()
        if checkbox_state == 1:
            self.textbox.pack_forget()
        else:
            self.webpage_btn.pack_forget()
            self.textbox.pack()
            self.webpage_btn.pack(pady="15")

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


cargo = CargoInterface()
cargo.mainloop()
