import customtkinter as ctk

from table_data import TableData
from webpage_loader import CargoWebpage
from dotenv import load_dotenv
import os
import tkinter as tk
import tkinter.messagebox as messagebox
import threading
from setting_window import SettingWindow
from utils import type_check
from webpage_data import WebpageData


class CargoInterface(ctk.CTk):
    """
    A GUI interface for generating Cargo Reports.

    This class creates a main window with 2 tabs: "SLA/Bot Report" and "Home Delivery".
    The "SLA/Bot Report" will include widgets for generating the SLA/Bot Report as well as some
    options you can configure, such as hiding the textbox or stopping the script.

    Main Operations:
        - stop_script(): Stop selenium script.
        - set_switch(): Toggle switch widgets on and off.
        - sla_bot_report_click(): Start selenium to generate the SLA/Bot Report
        - check_page_load(): Check to see if the page was loaded correctly in the script.
        - login_success(): Check if the script logged into successfully.
    """

    def __init__(self):
        super().__init__()
        self.webpage = CargoWebpage()
        self.title("Cargo Interface")
        self.geometry("500x500")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.resizable(False, False)

        self.setting_window = None

        self.webpage_data = WebpageData()

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

    @classmethod
    def set_switch(cls, status: bool, switch_widget: ctk.CTkSwitch, switch_str_var: ctk.StringVar, **kwargs):
        """
           Set switch widget to on or off, set text (optional) and enable/disable switch (optional).

           This method will check to ensure all arguments are the proper datatype. It will set the switch to on or off,
           allow optional text to be displayed next the switch and enable or disable the widget.

           Args:
               - status (bool): The status of the switch (on or off).
               - switch_widget (ctk.CTkSwitch): The switch widget to set.
               - switch_str_var(ctk.StringVar): The StringVar that handles the values of the on/off switch.
               - **kwargs: Additional keyword arguments that can be passed to the function.

           Keyword Args:
               - disable_widget (bool): Whether to disable the switch widget (default: None).
               - switch_text (str): The text to display on the switch widget (default: None).

           :returns:
               None
           """
        type_check(arg=status, arg_name="status", expected_type=bool)
        type_check(arg=switch_widget, arg_name="switch_widget", expected_type=ctk.CTkSwitch)

        disable_widget = kwargs.get("disable_widget", None)
        switch_text = kwargs.get("switch_text", None)

        if disable_widget is not None:
            type_check(arg=disable_widget, arg_name="disable_widget", expected_type=bool)
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

    def open_settings(self):
        """
        Open the Setting GUI Window.

        This method will open the setting GUI window which will allow the user to set certain settings for
        the SLA/Bot Report and Home Delivery Report.

        :return:
            None
        """
        if self.setting_window is None or not self.setting_window.winfo_exists():
            self.setting_window = SettingWindow()
            self.attributes("-topmost", False)

        else:
            self.setting_window.focus()
            self.attributes("-topmost", False)

    def hide_textbox(self):
        """
        Hide or Display the main textbox.

        This method will hide the textbox if the switch widget is set to "on". If the widget is set to "off",
        the textbox will be shown.

        :return:
            None
        """
        if self.hide_text_switch.get() == "on":
            self.textbox.pack_forget()
        else:
            self.webpage_btn.pack_forget()
            self.textbox.pack()
            self.webpage_btn.pack(pady="15")

    @classmethod
    def display_error(cls, title: str, message: str):
        """
        This will display a pop-up message to the user.

        This method allows you to customize your error message by setting the title and message for the pop-up box.

        :param title: Set the messagebox title.
        :param message: Set the messagebox message.
        :return: None
        """
        messagebox.showerror(title, message)

    def stop_script(self):
        """
        Stops the selenium script.

        This method sets the switch widget to "Script Not Running" and off and stops the selenium Script.
        It will quit the selenium browser as well.

        :returns:
            None
        """
        self.set_switch(status=False, switch_widget=self.script_switch, switch_str_var=self.script_running_var,
                        disable_widget=True, switch_text="Script Not Running")
        self.webpage.quit_selenium()

    def stop_script_command(self):
        """
        Create a new thread to stop the currently running Selenium script.

        This method creates a new thread to call the `stop_script` method,
        which will stop the currently running Selenium script. The new thread
        allows the user to continue interacting with the application while the
        script is stopped.

        :returns:
            None
        """
        thread = threading.Thread(target=self.stop_script)
        thread.start()

    def sla_bot_report_command(self):
        """
        Create new thread for starting the selenium script
        This method will allow the user to continue to interact with the GUI while the script is
        running in the background.

        :return:
            None
        """
        thread = threading.Thread(target=self.sla_bot_report_click)
        thread.start()

    # TODO: Add more detailed docstring once method is completed.
    def sla_bot_report_click(self):
        """Start selenium script to generate the SLA/Bot Report"""
        self.set_switch(status=True, switch_widget=self.script_switch, switch_str_var=self.script_running_var,
                        disable_widget=False, switch_text="Script Running")
        self.start_selenium()

        # Check all conditions. This will make sure nothing failed before making it to the "Airway bills to Ship Report"
        loading_waybill_page = all((self.starting_webpage_load(),
                                    self.login_success(),
                                    self.webpage.waybills_to_ship_page(self.webpage_data.get_waybill_url())))
        if loading_waybill_page:
            waybill_data, setting_day = self.webpage.fill_in_waybills_form()
            waybill_report = TableData(waybill_data)
            waybill_report.day_sorter = setting_day

            waybill_report.reformat_sla_bot_table()
            waybill_report.reformat_past_sla_data()

            waybill_report.sort_sla_bot_table()

            waybill_report.export_to_excel(waybill_report.table_data, "test.xlsx")

            self.set_switch(status=False, switch_widget=self.script_switch, switch_str_var=self.script_running_var,
                            disable_widget=True, switch_text="Script Not Running")

    def start_selenium(self):
        """
        Starts the selenium script and loads the starting webpage.

        This method starts the selenium webdriver script by calling the `start_selenium` method
        of the `webpage` object. It then loads the starting webpage by calling the `load_url` method
        with the `CARGO_HOMEPAGE` URL. It will retrieve the cargo homepage URL from the WebpageData class.

        :return:
            None
        """
        self.webpage.start_selenium()
        self.webpage.load_url(self.webpage_data.get_cargo_homepage())

    def starting_webpage_load(self) -> bool:
        """
        Checks if a webpage is loaded correctly.

        This method checks if a webpage is loaded correctly by calling the `check_webpage_loaded` method
        of the `webpage` object. If the webpage is not loaded correctly, it displays an error message
        using a pop-up window.

        Returns:
            bool: True if the webpage is loaded correctly, False otherwise.
        """
        # Check if starting webpage is loaded correctly. If it's not add a popup.
        if not self.webpage.check_webpage_loaded("//input[@id='UserName']", wait_time=5):
            messagebox.showerror("Webpage Load Error", "The webpage did not load correctly")
            return False
        return True

    def login_success(self) -> bool:
        """
        Try to log in and see if the script successfully logged in.

        This method trys to login and checks if the script was able to successfully log in by calling 'check_login'
        method of the 'webpage' object. If script is unable to login, it displays an error message using a pop-up window.
        :return:
            bool: True if the script successfully logged in, false otherwise.
        """

        self.webpage.login()

        # If login was unsuccessful provide popup.
        if not self.webpage.check_login():
            messagebox.showerror("Login Unsuccessful", "The login was unsuccessful")
            return False
        return True


cargo = CargoInterface()
cargo.mainloop()
