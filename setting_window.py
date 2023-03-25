import customtkinter as ctk
from Settings_Data import SettingsData
from tkinter import Button, Frame, messagebox, RIDGE


class SettingWindow(ctk.CTkToplevel):
    """
    A GUI interface for displaying script options.

    This class creates a main window with 2 different frames for settings. The 2 frames are SLA/Bot Settings and
    Home Delivery Settings. These 2 frames include entry boxes which loads the saved settings from a database. The
    user will be able to change the text in the entry box and save the settings to the database.

    Main Operations:
        - common_widgets_data(): Creates the data that is associated with widgets that are common in both SLA/Bot Settings and Home Delivery Settings
        - sla_bot_widgets_data(): Creates the data associated with only the SLA Settings
        - home_widgets_data(): Creates the data associated with only the Home Delivery Settings
        - insert_database_settings(widget_data, setting_group): Insert the saved setting data into the appropriate widget data (SLA/Bot Widgets| Home Delivery Widgets).
        - create_widgets(widget_data): Create widgets to be displayed on the GUI based on thewidget data (SLA/Bot Widgets | Home Delivery Widgets)
        - load_settings(setting_group, setting_name): Load the specified settings that were stored previously
        - save_sla_bot_settings(): Save SLA/Bot Settings to the database.
        - save_home_settings(): Save Home Delivery Settings to the database.
        - check_values(): Check which Setting Group (SLA/Bot Settings | Home Delivery Settings) has changed.
        Update the database for whichever setting has been changed.
    """

    def __init__(self):
        super().__init__()
        self.geometry("490x430")
        self.bind("<FocusIn>", self.on_focus_in)  # Focus in on window once its open.
        self.grab_set()  # Prevent main window from being usable until this window is closed.
        self.title("Settings")
        self.resizable(False, False)

        # Get Database Setting Data
        self.setting_data = SettingsData()
        self.bot_sla_data = self.setting_data.get_bot_sla_data()
        self.home_data = self.setting_data.get_home_delivery_data()

        # Create Frames, Button and Custom Menu Bar
        self.create_menu_bar_frame()
        self.create_menu_bar()
        self.create_main_frame()
        self.create_save_button()
        self.create_bot_sla_frame()
        self.create_home_delivery_frame()

        # Insert the widgets on Setting Window.
        # Widgets are being stored in a dictionary, so you can access the entry fields later on.
        self.widget_list = {
            "SLA/Bot Widgets": self.create_widgets(self.bot_sla_frame, self.sla_bot_widgets_data()),
            "Home Delivery Widgets": self.create_widgets(self.home_frame, self.home_widgets_data())
        }

        # Store the previous values
        self.previous_values = {
            "SLA/Bot Values": self.get_entry_box_values("SLA/Bot Widgets"),
            "Home Delivery Values": self.get_entry_box_values("Home Delivery Widgets")
        }

    def on_enter(self, event):
        """
        Change the background color of the "Help" button when hovering over it.

        This method changes the background color of the "Help" button when you hover your mouse over it.

        :param event: Required by the bind method call, but not used in the method body.
        :return: None
        """
        self.menu_bar['background'] = '#E5F3FF'

    def on_leave(self, event):
        """
        Change the background color of the "Help" button when the mouse is not hovering over button.

        This method changes the background color of the "Help" button when the mouse is not hovering over button.

        :param event: Required by the bind method call, but not used in the method body.
        :return: None
        """
        self.menu_bar['background'] = 'SystemButtonFace'

    def create_menu_bar_frame(self):
        """
        Create the Menu Bar Frame for the setting window.
        This method creates the Menu Bar Frame for the 'Help' Button.
        :return: None
        """
        self.menu_frame = Frame(master=self, height=20)
        self.menu_frame.pack(fill="both")

    def create_main_frame(self):
        """
        Creates the Main Frame of the Setting Window.
        This method creates the Main Frame of the setting window that will hold 2 different frames. The SLA/Bot Setting
        Frame and the Home Delivery Frame. It will also hold the Save Button widget.
        :return: None
        """
        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.pack()

    def create_bot_sla_frame(self):
        """
        Create the SLA/Bot Frame of the Setting Window
        This method creates the SLA/Bot Setting Frame. It will hold all the widgets that are associated with the
        SLA/Bot Settings.
        :return: None
        """
        self.bot_sla_frame = ctk.CTkFrame(master=self.main_frame, height=330)
        self.bot_sla_frame.pack_propagate(False)
        self.bot_sla_frame.pack(side="left", padx=(0, 30), pady=(20, 0))

    def create_home_delivery_frame(self):
        """
        Create the Home Delivery Frame of the Setting Window
        This method creates the Home Delivery Setting Frame. It will hold all the widgets that are associated with the
        Home Delivery Settings.
        :return: None
        """
        self.home_frame = ctk.CTkFrame(master=self.main_frame, height=330)
        self.home_frame.pack_propagate(False)
        self.home_frame.pack(side="left", pady=(20, 0))

    def create_menu_bar(self):
        """
        Creates the Custom Menu Bar.
        This method creates a custom menu bar, by using buttons on the create_menu_bar_frame.
        It creates a button to act as a menu bar item It uses bind methods, to change the hover affect when the
        mouse hovers over the button and when it leaves the button. It also provides a pop-up window when clicked.
        :return: None
        """
        self.menu_bar = Button(master=self.menu_frame, relief=RIDGE, text="Help", bd=0, command=self.help_pop_up)
        self.menu_bar.pack(side="left", padx=(5, 0))
        self.menu_bar.bind("<Enter>", self.on_enter)
        self.menu_bar.bind("<Leave>", self.on_leave)

    def help_pop_up(self):
        """
        Displays a pop-up messagebox.
        This method displays a pop-up messagebox with text displaying what each setting is used for. It is set
        to the parent frame to ensure no other windows can be clicked on.
        :return: None
        """

        # parent=self to ensure that this popup is on top of setting windows, due to bind.
        self.pop_up = messagebox.showinfo(title="Help Information", parent=self,
                                          message="Days:"
                                                  "\n"
                                                  "This is used to reformat the excel file for "
                                                  "sorting by the days to display in the Bot/SLA Report"
                                                  "\n"
                                                  "[Default Value: 8]"
                                                  "\n"
                                                  "\n"
                                                  "Number of Months Back:"
                                                  "\n"
                                                  "This is used to configure how many months "
                                                  "back you want the report to generate (starts from current month)"
                                                  "\n"
                                                  "[Default Value: Bot/SLA Report: '2' | Home Delivery Setting: '0']"
                                                  "\n"
                                                  "\n"
                                                  "Number of Days Back:"
                                                  "\n"
                                                  "This is used to configure how many days from "
                                                  "back you want the report to generate (starts from current day)"
                                                  "\n"
                                                  "[Default Value: Bot/SLA Report: '0' | Home Delivery Setting: '2']"
                                                  "\n"
                                                  "\n"
                                                  "From Airport:"
                                                  "\n"
                                                  "This is used to filter which airport you want to "
                                                  "generate the report from"
                                                  "\n"
                                                  "[Default Value: 'Please Select']"
                                                  "\n"
                                                  "\n"
                                                  "To Airport:"
                                                  "\n"
                                                  "This is used to filter which airport it should look for "
                                                  "when generating the report"
                                                  "\n"
                                                  "[Default Value: 'WPG']"
                                                  "\n"
                                                  "\n"
                                                  "Keyword:"
                                                  "\n"
                                                  "This is used to search by a certain keyword when "
                                                  "generating Home Delivery Setting"
                                                  "\n"
                                                  "[Default Value: 'SYSCO']")

    def create_save_button(self):
        """
        Creates a save button.
        This method creates a save button, which will allow all settings for each setting group (Home Delivery and
        SLA/Bot Settings) to be saved to a database.
        :return: None
        """
        save_button_frame = ctk.CTkFrame(master=self.main_frame, fg_color="transparent")
        save_button_frame.pack(side="bottom")

        self.save_button = ctk.CTkButton(master=save_button_frame, text="Save Settings", width=430,
                                         command=self.check_values)
        self.save_button.pack(pady="20")

    @classmethod
    def common_widgets_data(cls):
        """
        Store data for common widgets. Common widgets are widgets that display in both the Bot/SLA settings and
        Home Delivery Settings
        This method will store widget data for all common widgets. It will store the label text, entry_placeholder
        text, and the values that should be inserted into the widget box (setting_key).
        :return: Returns a list of Dictionaries.
        """
        widgets_data = [
            {"label_text": "Number of Months Back", "entry_placeholder": "2", "setting_key": "NumOfMonths"},
            {"label_text": "Number of Days Back", "entry_placeholder": "0", "setting_key": "NumOfDays"},
            {"label_text": "From Airport", "entry_placeholder": "WPG", "setting_key": "FromAirport"},
            {"label_text": "To Airport", "entry_placeholder": "Please Select", "setting_key": "ToAirport"},
        ]

        return widgets_data

    def sla_bot_widgets_data(self) -> list:
        """
        Stores the widget data for widgets only in the SLA/Bot Settings.
        This method will store widget data for SLA/Bot Settings. It will store the label text, entry_placeholder
        text, and the values that should be inserted into the widget box (setting_key). It also stores the
        label header text.

        The "insert_database_settings" method is used to update the "setting_key" values with the data
        from the database.

        :return: Returns a list of Dictionaries.
        """
        """Set the SLA/Bot Report Setting Widget Data"""
        sla_widget_data = [
            {"label_text": "Bot/SLA Report Settings"},
            {"label_text": "Days", "entry_placeholder": "8", "setting_key": "DayAmount"},
        ]

        new_sla_widgets = sla_widget_data + self.common_widgets_data()
        self.insert_database_settings(widget_data=new_sla_widgets, setting_group=self.bot_sla_data)

        return new_sla_widgets

    def home_widgets_data(self) -> list:
        """
        Stores the widget data for widgets only in the Home Delivery Settings.
        This method will store widget data for Home Delivery Settings. It will store the label text, entry_placeholder
        text, and the values that should be inserted into the widget box (setting_key). It also stores the
        label header text.

        The "insert_database_settings" method is used to update the "setting_key" values with the data
        from the database.

        :return: Returns a list of Dictionaries.
        """

        home_widget_data = [
            {"label_text": "Home Delivery Settings"},
            {"label_text": "Keyword", "entry_placeholder": "SYSCO", "setting_key": "Keyword"},
        ]

        new_home_widgets = home_widget_data + self.common_widgets_data()
        self.insert_database_settings(widget_data=new_home_widgets, setting_group=self.home_data)

        return new_home_widgets

    def insert_database_settings(self, widget_data: list, setting_group: dict):
        """
        Insert the settings that were retrieved from the database.

        This method will retrieve the settings that were pulled from the database. You will pass in the dictionary
        list of widgets as well as the appropriate dictionary that holds the database settings. There should be 2
        dictionaries. The bot_sla_data and home_data. Each one holds the specified values for Home Delivery Settings and
        SLA/Bot Settings.

        The method will also loop through all dictionary widgets while avoiding the first element, as that should be
        the label's header text.

        The "load_setting" method is used to retrieve the value of a setting from the specified setting group.

        :param widget_data: Pass in the dictionary list of widgets (ex. new_sla_widgets)
        :param setting_group: Select which dictionary to load. The dictionary will contain the values of the settings
        that were pulled from the database. Valid values are:
            - bot_sla_data and
            - home_data
        :return: None
        """

        # Enumerate to avoid access the first element in list, as that is header text.
        for index, data in enumerate(widget_data):
            if index != 0:
                data.update({"setting_key": self.load_setting(setting_group=setting_group,
                                                              setting_name=data["setting_key"])})

    @classmethod
    def create_widgets(cls, frame: ctk.CTkFrame, widget_data: list) -> dict:
        """
        Create all the widgets that were passed in and display them on the Setting Window.

        This method will loop through a list of widget_data and create the appropriate labels and entry fields along
        with the appropriate data that needs to be in each widget.

        It also creates an empty dictionary that will store all the entry boxes that were created. When the loop
        executes it will that empty dictonary with the keys being the label's text associated with the entry box and
        the values being the entry box object. (Ex. {Days: [Entry Box Object]}


        :param frame: Pass in the frame you want the widget to be created on.
        :param widget_data: List of widgets_data (ex. home_widgets_data()). This passes in all the home widgets data
        and creates the all the home widgets along with all the data that should be with those widgets.
        :return: Returns the widget_list dictionary.  Returns this, so you can access all the widget boxes that were
        created.
        """

        # Create a dictionary to store the entry widgets
        # The keys of the dictionary are the labels for that entry field in the widget_data list
        widget_list = {}

        # Using enumerate to access the first item in the list, as that will be the header text.
        for index, field in enumerate(widget_data):
            if index == 0:
                header_label = ctk.CTkLabel(master=frame, text=field["label_text"], font=("Helvetica", 12,
                                                                                          "bold", "underline"))
                header_label.pack()
            else:
                label = ctk.CTkLabel(master=frame, text=field["label_text"])
                label.pack()

                entry = ctk.CTkEntry(master=frame, width=100, justify="center",
                                     placeholder_text=field["entry_placeholder"])
                entry.insert(ctk.END, field["setting_key"])
                entry.pack()

                key = f"{field['label_text']}"
                widget_list[key] = entry

        return widget_list

    @classmethod
    def load_setting(cls, setting_group: dict, setting_name: str) -> str:
        """
        Loads the specified setting.

        This method loads the specified setting passed into the method. You will pass in the setting_group which will
        specify which dictionary to load. There should only be 2 dictionaries to load (bot_sla_data and home_data).
        These dictionaries contain the setting values that were pulled from the database. It also takes the setting_name
        which will take which specified setting you want to look at in the dictionary such as 'DayAmount' and look in
        the dictionary for that value.

        :param setting_group: Select which setting dictionary to load. Valid values are:
                              bot_sla_data and
                              home_data
        :param setting_name: Load the values of the specified settings.
                              Valid values are:
                              DayAmount,
                              NumOfMonths,
                              NumOfDays,
                              FromAirport,
                              ToAirport
                             If setting_group is home_delivery_settings, valid values are:
                              NumOfMonths,
                              NumOfDays,
                              FromAirport,
                              ToAirport,
                              Keywords
        :return: Returns the value for the specified setting name and setting group.
        """
        return setting_group[setting_name]

    def save_sla_bot_settings(self):
        """
        Update the SLA/Bot Setting Values to the database.

        This method will update the SLA/Bot Setting values to the appropriate table in the database.
        It will first get the value for each widget box in the SLA/Bot Settings Frame and pass that into
        the "setting_data" object and call the method "update_sla_bot_settings" which will update the database.

        :return: None
        """
        day_amount = self.widget_list["SLA/Bot Widgets"]["Days"].get()
        num_of_months = self.widget_list["SLA/Bot Widgets"]["Number of Months Back"].get()
        num_of_days = self.widget_list["SLA/Bot Widgets"]["Number of Days Back"].get()
        from_airport = self.widget_list["SLA/Bot Widgets"]["From Airport"].get()
        to_airport = self.widget_list["SLA/Bot Widgets"]["To Airport"].get()

        self.setting_data.update_database(table_name=self.setting_data.BOT_SLA_REPORT_TABLE_NAME,
                                          DayAmount=int(day_amount), NumOfMonths=int(num_of_months),
                                          NumOfDays=int(num_of_days), FromAirport=from_airport,
                                          ToAirport=to_airport)

    def save_home_settings(self):
        """
        Update the Home Delivery Setting Values to the database.

        This method will update the Delivery Setting values to the appropriate table in the database.
        It will first get the value for each widget box in the Delivery Setting Frame and pass that into
        the "setting_data" object and call the method "update_home_settings" which will update the database.

        :return: None
        """
        keyword = self.widget_list["Home Delivery Widgets"]["Keyword"].get()
        num_of_months = self.widget_list["Home Delivery Widgets"]["Number of Months Back"].get()
        num_of_days = self.widget_list["Home Delivery Widgets"]["Number of Days Back"].get()
        from_airport = self.widget_list["Home Delivery Widgets"]["From Airport"].get()
        to_airport = self.widget_list["Home Delivery Widgets"]["To Airport"].get()

        self.setting_data.update_database(table_name=self.setting_data.HOME_REPORT_TABLE_NAME, Keyword=keyword,
                                          NumOfMonths=int(num_of_months), NumOfDays=int(num_of_days),
                                          FromAirport=from_airport, ToAirport=to_airport)

    def get_entry_box_values(self, widget_group: str) -> dict:
        """
        Get the current entry box values.
        This method will get all the values in the entry box that is associated with the widget group. There should
        be only 2 groups of widgets: "SLA/Bot Widgets" or "Home Delivery Widgets" which can be access from the attribute
        widget_list.

        :param widget_group: Retrieve the specified setting's widget group's values.
                            valid values are:
                            SLA/Bot Widgets and
                            Home Delivery Widgets
        :return: Returns a dictionary of the widgets and their values. The key should be the widget's label text
        and the value will be the entry box value
        """
        widget_values = {key: value.get() for (key, value) in self.widget_list[widget_group].items()}
        return widget_values

    def check_values(self):
        """
        Compare the values of all entry boxes when the setting window is first loaded to when the save button is
        clicked. This will check which setting group was changed (SLA/Bot Setting or Home Delivery Setting). It will
        then update the database with the appropriate setting group.

        This method compares the values of all the entry boxes in each setting group from when the setting window
        is first opened to when the save button is clicked. There are 2 settings groups:
        SLA/Bot Setting or Home Delivery Setting. It will check the attribute previous_value first. The previous_value
        attribute stores all the entry box values when the setting window is first opened. The method will create a
        list of current_values which stores all the entry box values that are currently set. It will then compare to see
        if any entry box value is different from the previous_value. If there is a change it will update that setting
        group to the database as well update the previous_values to current_values.

        :return: None
        """

        current_values = {
            "SLA/Bot Values": self.get_entry_box_values("SLA/Bot Widgets"),
            "Home Delivery Values": self.get_entry_box_values("Home Delivery Widgets")
        }

        if current_values["SLA/Bot Values"] != self.previous_values["SLA/Bot Values"]:
            self.previous_values = current_values
            self.save_sla_bot_settings()

        if current_values["Home Delivery Values"] != self.previous_values["Home Delivery Values"]:
            self.previous_values = current_values
            self.save_home_settings()

    def on_focus_in(self, event):
        """
        Bring the Setting Window in front of the Main GUI Window.
        :param event: Required by the bind method call, but not used in the method body.
        :return: None
        """
        self.attributes("-topmost", True)
