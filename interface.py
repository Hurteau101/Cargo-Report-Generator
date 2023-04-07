from typing import Union, Optional, Type
from datetime import datetime
import threading
import customtkinter as ctk
import pandas as pd
from selenium.common import NoSuchElementException, TimeoutException
from error_window import ErrorWindow
from report_design import ReportDesign
from table_data import TableData
from webpage_loader import CargoWebpage
from setting_window import SettingWindow
from webpage_data import WebpageData
from utils import type_check
from webpage_settings import WebpageSettings


class CargoInterface(ctk.CTk):
    """
    The main GUI for the Cargo Report Generator.
    """

    VALID_REPORTS = ["SLA/Bot Report", "Home Delivery Report"]

    def __init__(self):
        """
        Initializes a CargoInterface Object.

        Creates all the necessary Widgets/Frames to display the CargoInterface Window.
        """
        super().__init__()
        self.webpage = CargoWebpage()
        self.webpage_data = WebpageData()
        self.title("Cargo Script")
        self.geometry("370x580")
        self.resizable(False, False)
        self.iconbitmap("icon.ico")

        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("green")

        self.setting_window: Optional[SettingWindow] = None
        self.error_window: Optional[ErrorWindow] = None

        # Main Frame
        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.pack(fill="both", pady=(20, 0))

        # Script Frame
        self.script_frame = ctk.CTkFrame(master=self.main_frame, height=300, width=330)
        self.script_frame.pack_propagate(False)
        self.script_frame.pack(side="top")

        # Textbox Widget
        self.textbox = ctk.CTkTextbox(master=self.script_frame, width=300, state=ctk.DISABLED)
        self.textbox.pack_propagate(False)
        self.textbox.pack(side="top", pady=(15, 12))

        # Selection Frame (This frame is created to align the button and option menu side by side)
        self.selection_frame = ctk.CTkFrame(master=self.script_frame, fg_color="transparent")
        self.selection_frame.pack(fill="x")

        # Selection Widgets
        self.load_script_btn = ctk.CTkButton(master=self.selection_frame, text="Report Loader", width=120,
                                             command=self.script_selection)
        self.load_script_btn.pack(side="left", padx="19", pady="15", anchor="center")

        self.script_option_var = ctk.StringVar(value="SLA/Bot Report")
        self.script_selection_menu = ctk.CTkOptionMenu(master=self.selection_frame,
                                                       values=["SLA/Bot Report", "Home Delivery Report"],
                                                       variable=self.script_option_var, anchor="center", width=150)
        self.script_selection_menu.pack(side="left")

        # Option Frame
        self.option_frame = ctk.CTkFrame(master=self.main_frame, height=270, width=330)
        self.option_frame.pack_propagate(False)
        self.option_frame.pack(side="top", pady="20")

        # Label Widget
        self.option_label = ctk.CTkLabel(master=self.option_frame, text="Options:", font=("Helvetica", 20, "bold"))
        self.option_label.pack(side="top", pady=(15, 20))

        # Switch Frame
        self.switch_frame = ctk.CTkFrame(master=self.option_frame, fg_color="transparent")
        self.switch_frame.pack(side="top")

        # Switch Widgets
        self.hide_tb_var = ctk.StringVar(value="off")
        self.hide_tb_switch = ctk.CTkSwitch(master=self.switch_frame, text="Hide Textbox", variable=self.hide_tb_var,
                                            onvalue="on", offvalue="off", command=self.hide_textbox)
        self.hide_tb_switch.pack(side="left", padx="20")

        self.script_status_var = ctk.StringVar(value="off")
        self.script_status_switch = ctk.CTkSwitch(master=self.switch_frame, text="Script OFF",
                                                  variable=self.script_status_var,
                                                  onvalue="on", offvalue="off", state=ctk.DISABLED,
                                                  command=lambda: self.create_thread(
                                                      target=self.stop_script_configuration))
        self.script_status_switch.pack(side="left")

        # Setting Frame
        self.setting_frame = ctk.CTkFrame(master=self.option_frame, fg_color="transparent")
        self.setting_frame.pack(side="top")

        # Setting Button
        self.open_setting_btn = ctk.CTkButton(master=self.setting_frame, text="Open Settings", width=300,
                                              command=lambda: self.open_new_window(window=self.setting_window,
                                                                                   window_class=SettingWindow,
                                                                                   theme=self.appearance_option.get(),
                                                                                   title="Settings", size="490x430"))

        self.open_setting_btn.pack(side="top", pady="20")

        # Appearance Frame
        self.appearance_frame = ctk.CTkFrame(master=self.option_frame, fg_color="transparent")
        self.appearance_frame.pack(side="top", pady=15)

        # Appearance Widgets
        self.appearance_label = ctk.CTkLabel(master=self.appearance_frame, text="Appearance:",
                                             font=("Helvetica", 15, "bold"))
        self.appearance_label.pack(side="left", padx="20")

        self.appearance_option = ctk.CTkOptionMenu(master=self.appearance_frame,
                                                   values=["Dark", "Light", "System"],
                                                   anchor="center", width=150, command=CargoInterface.set_appearance)
        self.appearance_option.pack(side="left")

    @classmethod
    def set_appearance(cls, new_appearance: str) -> None:
        """
        Set the appearance of the GUI.
        :param new_appearance: Appearance text of the appearance selection.
        """
        ctk.set_appearance_mode(new_appearance)

    @classmethod
    def set_switch(cls, status: bool, switch_widget: ctk.CTkSwitch, switch_str_var: ctk.StringVar, **kwargs) -> None:

        """
        Set switch widget to on or off, set text (optional) and enable/disable switch (optional).

        This will set the switch to on or off, allow optional text to be displayed next the switch and
        enable or disable the widget.

            Args:
              - status (bool): The status of the switch (on or off).
              - switch_widget (ctk.CTkSwitch): The switch widget to set.
              - switch_str_var(ctk.StringVar): The StringVar that handles the values of the on/off switch.
              - **kwargs: Additional keyword arguments that can be passed to the function.
            Keyword Args:
              - disable_widget (bool): Whether to disable the switch widget (default: None).
              - switch_text (str): The text to display on the switch widget (default: None).
            Raise:
              - TypeError: If the status of the widget is not of type Bool or if a switch is not of type CTKSwitch
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

    def script_selection(self) -> None:
        """
        Gets the value of the Script Selection dropdown menu. This will determine which script to run.
        """
        if self.script_selection_menu.get() == "SLA/Bot Report":
            self.create_thread(target=self.generate_sla_bot_report)
        else:
            self.create_thread(target=self.generate_home_delivery_report)

    def open_new_window(self, window: Optional[Union[SettingWindow, ErrorWindow]],
                        window_class: Union[Type[SettingWindow], Type[ErrorWindow]], theme: str, size: str, title: str,
                        **kwargs):
        """
        Opens a new window, dependent on the class passed in.

            Args:
                - window: The instance attribute for the window you want.
                - status (bool): The status of the switch (on or off).
                - window_class: The class for the Window you want opened.
                - theme: The theme for the window.
                - kwargs: Additional keyword arguments that can be passed to the function.

           Keyword Args:
                - title = Set the title of the window.
                - error_message = Set error message for the window.
        """

        if window is None or not window.winfo_exists():
            window = window_class(theme=theme, size=size, title=title, **kwargs)
            self.attributes("-topmost", False)
        else:
            self.setting_window.focus()
            self.attributes("-topmost", False)

    def insert_text(self, message: str, color: str = "#FFFFFF") -> None:
        """
        Inserts text into the text box with a specific text color.
        :param color: Color of text. (Default: '#FFFFFF' (White))
        :param message: Message to pass into the textbox.
        """

        self.textbox.configure(state=ctk.NORMAL, text_color=color)

        if color is not None:
            self.textbox.configure(text_color=color)
            self.textbox.insert(ctk.END, f"{message}\n")
        else:
            self.textbox.insert(ctk.END, f"{message}\n")

        self.textbox.configure(state=ctk.DISABLED)

    def clear_text(self) -> None:
        """
        Clears the text in the textbox.
        """
        self.textbox.configure(state=ctk.NORMAL)
        self.textbox.delete("1.0", ctk.END)
        self.textbox.configure(state=ctk.DISABLED)

    def hide_textbox(self) -> None:
        """
        Hides the textbox once switch is set to ON. Once the switch is set to OFF it will repack all items,
        to get the layout how it was before.
        """
        if self.hide_tb_var.get() == "on":
            self.textbox.pack_forget()
            self.script_frame.configure(height=65)
            self.script_frame.pack_propagate(False)
            self.geometry("370x400")

        else:
            self.load_script_btn.pack_forget()
            self.script_selection_menu.pack_forget()
            self.script_frame.configure(height=300)
            self.selection_frame.pack_forget()
            self.textbox.pack(side="top", pady=(15, 12))
            self.selection_frame.pack(fill="x")
            self.load_script_btn.pack()
            self.load_script_btn.pack(side="left", padx="19", pady="15", anchor="center")
            self.script_selection_menu.pack(side="left")
            self.geometry("370x580")

    def display_error(self, title: str, message: str) -> None:
        """
        Creates an error message window.

        This method will create a custom error message window. It will turn the script switch off and re-enable
        the Generate report button
        :param title: Title of error window.
        :param message: Message to display in the error window.
        """
        self.open_new_window(window=self.error_window, window_class=ErrorWindow, theme=self.appearance_option.get(),
                             size="300x200", title=title, error_message=message)
        self.clear_text()
        self.insert_text("There was an error. Please try again.", color="red")
        self.stop_script_configuration()

    def load_error(self, name_of_webpage: str) -> None:
        """
        Error message specific to the webpage that had an issue loading.

        This method will display an error message of "There was a problem loading the {name_of_webpage} page.
        Please try re-running the script."

        :param name_of_webpage: Name of the webpage that wasn't loaded correctly.
        """
        self.display_error(title="Load Error", message=f"There was a problem loading the {name_of_webpage} page. \n"
                                                       "Please try re-running the script.")

    def form_error(self, exception: Exception) -> None:
        """
        Handles errors that happen when the script is filling in a form on the cargo website.
        :param exception: Exception that was thrown.
        """
        self.webpage.quit_selenium()

        if isinstance(exception, TimeoutException):
            self.display_error(title="No Data Error", message="Script was unable to find any data."
                                                              "\n"
                                                              "\n"
                                                              "If you are running the SLA/Bot Report this error could"
                                                              " be caused by the script loading to slowly."
                                                              "\n"
                                                              "\n"
                                                              "If you are running the Home Delivery Report this error"
                                                              " could be caused by not finding any AWB's. Check your "
                                                              "'keyword' in the settings window. If 'keyword' looks"
                                                              " correct, then this is caused by the script loading to"
                                                              " slowly."
                                                              "\n"
                                                              "\n"
                                                              "Please try again")
        if isinstance(exception, NoSuchElementException):
            self.display_error(title="No Data Error", message="No data was found. Common issue could be the "
                                                              "'To Airport' or/and 'From Airport' "
                                                              "in the settings window is an invalid airport."
                                                              "Please try re-running the script.")

    @staticmethod
    def create_thread(target: callable) -> None:
        """
        Creates a thread.
        :param target: The method you want to start a thread on.
        """
        thread = threading.Thread(target=target)
        thread.start()

    @staticmethod
    def set_button_state(button_state: bool, button: ctk.CTkButton) -> None:
        """
        Set a buttons state. (Enabled or Disabled)
        :param button_state: State of the button (Enabled [True] or Disabled [False])
        :param button: Which button state to change.
        :raises TypeError: Will raise an error if button_state is not of type bool and/or if button is not of
            type CTkButton
        """

        type_check(arg=button_state, arg_name="button_state", expected_type=bool)
        type_check(arg=button, arg_name="button", expected_type=ctk.CTkButton)

        if button_state:
            button.configure(state=ctk.NORMAL)
        else:
            button.configure(state=ctk.DISABLED)

    def start_script_configuration(self) -> None:
        """
        Configure widgets for when the script starts running

        This will configure the button to disabled and set the script running switch to ON.
        """
        self.set_button_state(button_state=False, button=self.load_script_btn)
        self.set_switch(status=True, switch_widget=self.script_status_switch, switch_str_var=self.script_status_var,
                        disable_widget=False, switch_text="Script ON")

    def start_script(self) -> None:
        """
        Starts the Selenium script and loads the starting webpage.

        This will start the script and configure all widgets to the necessary state while the script is running.
        """
        self.clear_text()
        self.insert_text("Starting Script.")
        self.webpage.start_selenium(options=WebpageSettings.headless_chrome())
        self.start_script_configuration()
        self.insert_text("Loading Cargo Webpage.")
        self.webpage.load_url(self.webpage_data.get_cargo_homepage())

    def stop_script_configuration(self) -> None:
        """
        Configure widgets for when the script stops running and set state of widgets.
        """
        self.set_switch(status=False, switch_widget=self.script_status_switch, switch_str_var=self.script_status_var,
                        disable_widget=True, switch_text="Script OFF")

        self.set_button_state(button_state=True, button=self.load_script_btn)

        if self.webpage.script_running:
            self.webpage.quit_selenium()

    def generate_sla_bot_report(self) -> None:
        """
        Extract's data from the Cargo webpage and creates the SLA/Bot Report.
        """
        self.start_script()
        if self.script_loaded_properly():
            self.insert_text("Login Successful.")
            if self.webpage.check_waybills_to_ship_page(self.webpage_data.get_waybill_url()):
                try:
                    html_table, day_setting = self.webpage.fill_in_waybills_form()
                    self.insert_text("Extracting Waybills to Ship Data.")
                except TimeoutException as exception:
                    self.form_error(exception)
                except NoSuchElementException as exception:
                    self.form_error(exception)
                else:
                    sla_dict, bot_df, highest_day = CargoInterface.get_sla_bot_data(html_table=html_table,
                                                                                    day_setting=day_setting)
                    self.insert_text("Designing SLA/Bot Report.")
                    self.create_sla_bot_report(sla_dict=sla_dict, bot_df=bot_df, day_sorter=day_setting,
                                               highest_day=highest_day)

                    self.stop_script_configuration()
                    self.insert_text(f"SLA/Bot Report created at {CargoInterface.get_created_time()}.")
            else:
                self.load_error(name_of_webpage="waybills to ship")

    @staticmethod
    def get_created_time() -> str:
        """
        Get current time formatted.
        :return: Returns formatted time.
        """
        today_date = datetime.now()
        format_time = today_date.strftime("%I:%M %p")
        return format_time

    def generate_home_delivery_report(self) -> None:
        """
        Extract's data from the Cargo webpage and creates the Home Delivery Report.
        """
        self.start_script()
        if self.script_loaded_properly():
            self.insert_text("Login Successful.")
            if self.webpage.check_search_awbs_page(self.webpage_data.get_search_awb_url()):
                try:
                    self.insert_text("Obtaining list of AWB's.")
                    html_table = self.webpage.fill_in_search_form()
                except TimeoutException as exception:
                    self.form_error(exception)
                else:
                    self.insert_text("Extracting Home Delivery AWB's. Please wait..")
                    shipped_awb_df, non_shipped_df = self.get_home_delivery_data(html_table=html_table)
                    self.insert_text("Designing Home Delivery Report.")
                    self.create_home_delivery_report(shipped_awb_df=shipped_awb_df, non_shipped_awb_df=non_shipped_df)

                    self.stop_script_configuration()
                    self.insert_text(f"Home Delivery Report created at {CargoInterface.get_created_time()}.")
            else:
                self.load_error(name_of_webpage="Search AWB")

    @classmethod
    def get_sla_bot_data(cls, html_table, day_setting) -> tuple[dict, pd.DataFrame, int]:
        """
        Get the SLA/Bot Report Data.

        Method is responsible for creating the TableData Object for extracting the necessary data to create
        the SLA/Bot Report.
        :param html_table: The HTML Table to extract.
        :param day_setting: The value for "DayAmount" in the Database.
        :return: Returns a tuple of data for SLA Data, Bot Dataframe and Highest Day value.
        """
        sla_bot_data = TableData(table_data=html_table, report_name=cls.VALID_REPORTS[0])
        sla_bot_data.day_sorter = day_setting
        sla_bot_data.create_report_data(cls.VALID_REPORTS[0])
        sla_data, bot_df, highest_day = sla_bot_data.get_sla_bot_data()
        return sla_data, bot_df, highest_day

    @classmethod
    def create_sla_bot_report(cls, sla_dict: dict, bot_df: pd.DataFrame, highest_day, day_sorter) -> None:
        """
        Creates the SLA/Bot Report.

        Method is responsible for creating the ReportDesign Object for designing the SLA/Bot Report Data.
        :param sla_dict: SLA Dictionary.
        :param bot_df: Bot Report Dataframe
        :param highest_day: The highest day value.
        :param day_sorter: The Day Sorter value (pulled from Database)
        """
        report_design = ReportDesign(report_name=cls.VALID_REPORTS[0])
        report_design.sla_data = sla_dict
        report_design.bot_df = bot_df
        report_design.day_sorter = day_sorter * -1
        report_design.highest_day = highest_day
        report_design.create_report(report_name=cls.VALID_REPORTS[0])

    def get_home_delivery_data(self, html_table) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Get the Home Delivery Report Data.

        :param html_table: The HTML Table to extract.
        :return: Returns a tuple of shipped AWB dataframe and non-shipped awb Dataframe.
        """
        home_delivery_data = TableData(table_data=html_table, report_name=self.VALID_REPORTS[1])
        awb_list = home_delivery_data.get_awb_list()
        home_delivery_awbs = self.webpage.search_awb(awb_list=awb_list)

        home_delivery_data.home_delivery_awb_list = home_delivery_awbs
        home_delivery_data.create_report_data(self.VALID_REPORTS[1])
        shipped_awb_df, non_shipped_df = home_delivery_data.get_home_delivery_data()
        return shipped_awb_df, non_shipped_df

    @classmethod
    def create_home_delivery_report(cls, shipped_awb_df: pd.DataFrame, non_shipped_awb_df: pd.DataFrame) -> None:
        """
        Creates the Home Delivery Report.

        :param shipped_awb_df: The shipped AWB Dataframe.
        :param non_shipped_awb_df: The non-shipped AWB dataframe.
        """
        report_design = ReportDesign(report_name=cls.VALID_REPORTS[1])
        report_design.shipped_awb_df = shipped_awb_df
        report_design.non_shipped_awb_df = non_shipped_awb_df
        report_design.create_report(report_name=cls.VALID_REPORTS[1])

    def script_loaded_properly(self) -> bool:
        """
        Checks to see if the starting portion of loading the script is loaded properly.

        This will check if the homepage was loaded correctly and if login was successful.
        :return: Returns True if script was loaded correctly, otherwise False.
        """

        is_loaded = all((self.check_homepage_loaded(), self.check_login_success()))
        return is_loaded

    def check_homepage_loaded(self, wait_time: int = 5) -> bool:
        """
        Check if the Cargo homepage was loaded correctly.

        This will check to see if an element on the cargo homepage is visible. If it is, then the homepage loaded
        correctly.
        :param wait_time: Length of time (seconds) to wait to see if the element is visible (Default: 5)
        :return: Returns true if it can find the element, otherwise False.
        """
        if not self.webpage.check_element_loaded("//input[@id='UserName']", wait_time=wait_time):
            self.load_error(name_of_webpage="home")
            return False

        return True

    def check_login_success(self) -> bool:
        """
        Logins into the cargo webpage and checks if the login was successful.
        :return: Returns True if it was able to log in successfully, otherwise False.
        """
        self.webpage.login()

        if not self.webpage.check_login():
            self.display_error(title="Login Error", message="There was a problem logging into the webpage. "
                                                            "Please try re-running the script.")
            return False
        return True


if __name__ == "__main__":
    cargo = CargoInterface()
    cargo.mainloop()
