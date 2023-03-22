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

        self.hide_text_var = ctk.StringVar(value="off")
        self.hide_text_switch = ctk.CTkSwitch(master=self.option_frame, text="Hide Textbox",
                                          command=self.hide_textbox, variable=self.hide_text_var, onvalue="on",
                                          offvalue="off")
        self.hide_text_switch.pack()

        self.script_running_var = ctk.StringVar(value="off")
        self.script_switch = ctk.CTkSwitch(master=self.option_frame, text="Script Off",
                                           command=self.stop_script_command, variable=self.script_running_var,
                                           onvalue="on",
                                           offvalue="off", state=ctk.DISABLED)
        self.script_switch.pack()

    def stop_script(self):
        """Stop selenium script"""
        self.set_switch(status=False, switch_widget=self.script_switch, switch_str_var=self.script_running_var,
                        disable_widget=True, switch_text="Script Not Running")
        self.webpage.quit_selenium()

    def stop_script_command(self):
        """Create new thread for stopping selenium"""
        thread = threading.Thread(target=self.stop_script)
        thread.start()

    @classmethod
    def type_check(cls, arg, arg_name: str, expected_type: type):
        """Check the type of argument. Raise an error, if the argument is not what is expected"""
        if not isinstance(arg, expected_type):
            raise TypeError(f"Expected '{arg_name}' to be of type '{expected_type.__name__}' "
                            f"but got '{type(arg).__name__}' instead")

    def set_switch(self, status: bool, switch_widget: ctk.CTkSwitch, switch_str_var: ctk.StringVar, **kwargs):
        """
           Set switch widget to on or off.

           Args:
               status (bool): The status of the switch (on or off).
               switch_widget (ctk.CTkSwitch): The switch widget to set.
               switch_str_var(ctk.StringVar): The StringVar that handles the values of the on/off switch.
               **kwargs: Additional keyword arguments that can be passed to the function.

           Keyword Args:
               disable_widget (bool): Whether to disable the switch widget (default: None).
               switch_text (str): The text to display on the switch widget (default: None).
           """
        self.type_check(arg=status, arg_name="status", expected_type=bool)
        self.type_check(arg=switch_widget, arg_name="switch_widget", expected_type=ctk.CTkSwitch)

        disable_widget = kwargs.get("disable_widget", None)
        switch_text = kwargs.get("switch_text", None)

        if disable_widget is not None:
            self.type_check(arg=disable_widget, arg_name="disable_widget", expected_type=bool)
            if disable_widget:
                switch_widget.configure(state=ctk.DISABLED)
            else:
                switch_widget.configure(state=ctk.NORMAL)

        if switch_text is not None:
            switch_widget.configure(text=switch_text)

        if status:
            switch_str_var.set(value="on")
        else:
            switch_str_var.set(value="off")

    def sla_bot_report_command(self):
        """Create new thread for starting webscraper"""
        thread = threading.Thread(target=self.sla_bot_report_click)
        thread.start()

    def sla_bot_report_click(self):
        self.set_switch(status=True, switch_widget=self.script_switch, switch_str_var=self.script_running_var,
                        disable_widget=False, switch_text="Script Running")
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
        if self.hide_text_switch.get() == "on":
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
