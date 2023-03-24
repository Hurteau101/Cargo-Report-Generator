import customtkinter as ctk
from Settings_Data import SettingsData


class SettingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("490x470")
        self.bind("<FocusIn>", self.on_focus_in)  # Focus in on window once its open.
        self.grab_set()  # Prevent main window from being usable until this window is closed.
        self.title("Settings")
        self.resizable(False, False)

        # Get Settings Data
        self.setting_data = SettingsData()
        self.bot_sla_data = self.setting_data.get_bot_sla_data()
        self.home_data = self.setting_data.get_home_delivery_data()

        # Create Frames
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

        self.save_button = ctk.CTkButton(master=save_button_frame, text="Save Settings", width=430,
                                         command=self.save_setting)
        self.save_button.pack(pady="20")

    @classmethod
    def common_widgets_data(cls):
        widgets_data = [
            {"label_text": "Number of Months Back", "entry_placeholder": "2", "setting_key": "NumOfMonths"},
            {"label_text": "Number of Days Back", "entry_placeholder": "0", "setting_key": "NumOfDays"},
            {"label_text": "From Airport", "entry_placeholder": "WPG", "setting_key": "FromAirport"},
            {"label_text": "To Airport", "entry_placeholder": "Please Select", "setting_key": "ToAirport"},
        ]

        return widgets_data

    def sla_bot_widgets_data(self):
        """Set the SLA/Bot Report Setting Widget Data"""
        sla_widget_data = [
            {"label_text": "Bot/SLA Report Settings"},
            {"label_text": "Days", "entry_placeholder": "8", "setting_key": "DayAmount"},
        ]

        new_sla_widgets = sla_widget_data + self.common_widgets_data()
        self.insert_database_settings(widget_data=new_sla_widgets, setting_group=self.bot_sla_data)

        return new_sla_widgets

    def home_widgets_data(self):
        """Set the Home Delivery Report Setting Widget Data"""
        home_widget_data = [
            {"label_text": "Home Delivery Settings"},
            {"label_text": "Keyword", "entry_placeholder": "SYSCO", "setting_key": "Keyword"},
        ]

        new_home_widgets = home_widget_data + self.common_widgets_data()
        self.insert_database_settings(widget_data=new_home_widgets, setting_group=self.home_data)

        return new_home_widgets

    def insert_database_settings(self, widget_data, setting_group):
        """Insert the settings that were retrieved from the database.
            :param widget_data: Dictionary list of widgets
            :param setting_group: Select which setting dictionary to load. Valid values are:
                              bot_sla_data and
                              home_data
        """
        # Enumerate to avoid access the first element in list, as that is header text.
        for index, data in enumerate(widget_data):
            if index != 0:
                data.update({"setting_key": self.load_setting(setting_group=setting_group,
                                                              setting_name=data["setting_key"])})

    @classmethod
    def create_widgets(cls, frame, widget_data):
        """Insert all the widgets on setting screen"""

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
    def load_setting(cls, setting_group: dict, setting_name: str):
        """
        Load the specified setting.

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
        :return: Returns the value for the specified setting name.
        """
        return setting_group[setting_name]

    def save_sla_bot_settings(self):
        """Update SLA/Bot Setting Database values."""
        day_amount = self.widget_list["SLA/Bot Widgets"]["Days"].get()
        num_of_months = self.widget_list["SLA/Bot Widgets"]["Number of Months Back"].get()
        num_of_days = self.widget_list["SLA/Bot Widgets"]["Number of Days Back"].get()
        from_airport = self.widget_list["SLA/Bot Widgets"]["From Airport"].get()
        to_airport = self.widget_list["SLA/Bot Widgets"]["To Airport"].get()

        self.setting_data.update_sla_bot_settings(table_name=self.setting_data.BOT_SLA_REPORT_TABLE_NAME,
                                                  DayAmount=int(day_amount), NumOfMonths=int(num_of_months),
                                                  NumOfDays=int(num_of_days), FromAirport=from_airport,
                                                  ToAirport=to_airport)

    def save_home_settings(self):
        """Update Home Setting Database values."""
        keyword = self.widget_list["Home Delivery Widgets"]["Keyword"].get()
        num_of_months = self.widget_list["Home Delivery Widgets"]["Number of Months Back"].get()
        num_of_days = self.widget_list["Home Delivery Widgets"]["Number of Days Back"].get()
        from_airport = self.widget_list["Home Delivery Widgets"]["From Airport"].get()
        to_airport = self.widget_list["Home Delivery Widgets"]["To Airport"].get()

        self.setting_data.update_home_settings(table_name=self.setting_data.HOME_REPORT_TABLE_NAME, Keyword=keyword,
                                               NumOfMonths=int(num_of_months), NumOfDays=int(num_of_days),
                                               FromAirport=from_airport, ToAirport=to_airport)

    def get_entry_box_values(self, widget_group):
        """
        Get the current entry box values.
        :param widget_group: Retrieve the specified setting's widget group's values.
                            valid values are:
                            SLA/Bot Widgets and
                            Home Delivery Widgets
        :return: return all current entry box values.
        """
        widget_values = {key: value.get() for (key, value) in self.widget_list[widget_group].items()}
        return widget_values

    def save_setting(self):
        """
        Check which setting group was changed. If setting group was changed, then update that setting group to database
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

    #TODO: Update entry box values once settings are saved.

    def on_focus_in(self, event):
        """Bring setting window to the front when opened"""
        self.attributes("-topmost", True)
