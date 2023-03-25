from dateutil.relativedelta import relativedelta
from datetime import date
from dotenv import load_dotenv
import os
import pandas as pd

from Settings_Data import SettingsData

load_dotenv()
USERNAME = os.getenv("USERNAME_1")
PASSWORD = os.getenv("PASSWORD")
CARGO_HOMEPAGE = os.getenv("CARGO_HOMEPAGE")
WAYBILLS_REPORT_URL = os.getenv("WAYBILLS_REPORT_URL")


class WebpageData:
    def __init__(self):
        self.sla_bot_data = None
        self._username = USERNAME
        self._password = PASSWORD
        self._cargo_homepage = CARGO_HOMEPAGE
        self._waybill_url = WAYBILLS_REPORT_URL

    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_cargo_homepage(self):
        return self._cargo_homepage

    def get_waybill_url(self):
        return self._waybill_url

    @classmethod
    def subtract_date(cls, months: int = 0, days: int = 0):
        """
        Subtracts the current date by the amount of months set and days set. Default value for months and days is 0
        This method will take the current day and subtract is by the amount of months and days passed in from
        the argument. It will then reformat that date object into a string with a specific format (Ex. 25-Mar-2023)

        :param months: Amount of months you want to subtract from the current date. Default value is 0.
        :param days: Amount of days you want to subtract from the current date. Default value is 0.
        :return: Returns the date as a reformatted string. (Ex. 25-Mar-2023)
        """
        today_date = date.today()
        new_date_object = today_date + relativedelta(months=-months, days=-days)
        new_date_string = new_date_object.strftime('%d-%b-%Y')

        return new_date_string

    def get_setting_values(self, setting_group: str):
        """
        Get the settings values for a specific setting group. Pass in either "SLA/Bot" or "Home".

        This method will get the setting values which are stored in a database. It will obtain the values based on
        "SLA/Bot" or "Home" which you will pass in as an argument. It will also update the dictionary to add a
        new item of Date to the dictionary to be used to fill in a "From Date" form from the webpage.

        :param setting_group: Pass in which settings you want to update. Either "SLA/Bot" or "Home".
        :return: Returns a dictionary of the settings.
        """

        settings = SettingsData()

        if setting_group.upper() == "SLA":
            sla_dict = settings.get_bot_sla_data()
            self.update_setting_dictionary(sla_dict)
            return sla_dict
        elif setting_group.upper() == "HOME":
            home_dict = settings.get_home_delivery_data()
            self.update_setting_dictionary(home_dict)
            return home_dict
        else:
            raise ValueError(f"{setting_group} is not a valid setting group. Please only pass in 'SLA' or 'Home'")

    def update_setting_dictionary(self, setting_dict):
        """
        Update the appropriate values in setting dictionary that is passed in as the argument.
        This method updates any dictionary that needs to be updated with specific values, so that when the dictionary
        is called later on to fill in a form, no value errors are provided by selenium.

        :param setting_dict: Pass in which setting dictionary to update. Should be either SLA/Bot Report Setting or
        Home Delivery Setting Dictionary
        :return: None
        """
        self.update_date_settings(setting_dict)
        self.update_airport_dictionary(setting_dict)

    @classmethod
    def update_airport_dictionary(cls, setting_dict: dict):
        """
        Checks the dictionary key of "ToAirport" and "FromAirport" to see if the value is "Please Select". If it is
        it updates its value to 0.

        This method checks to see if the dictionary key of the passed in setting dictionary for "ToAirport" and
        "FromAirport" values are "Please Select". If they are, they will be changed to 0. The reason for this, is the
        drop-down for each of the airport's "Please Select" value isn't actually "Please Select". The value is
        associated with 0 instead. This will prevent errors of not finding that value.

        :param setting_dict: Pass in which setting dictionary to update. Should be either SLA/Bot Report Setting or
        Home Delivery Setting Dictionary.
        :return: None
        """
        to_airport = setting_dict["ToAirport"]

        if to_airport == "Please Select":
            setting_dict["ToAirport"] = "0"

    def update_date_settings(self, setting_dict: dict):
        """
        Add a configured date to the specific setting_dict. (Ex. Date: 25-Mar-2023 added to dictionary)
        This method will add a new date string to the specified dictionary. This new date will be used on the Cargo
        Webpage that requires you to fill in "From Date". We are using the settings of NumOfMonths which is used to
        decide how many months back to go from the current date and NumOfDays which is used to decide how many days
        to go back from the current date. Using that information, this method can create a date item in the dictionary.
        :param setting_dict: Pass in the appropriate setting dictionary. Valid values are sla_bot_setting_data or
        sla_bot_setting_data dictionary attribute.

        :return: None
        """
        num_of_months = setting_dict["NumOfMonths"]
        num_of_days = setting_dict["NumOfDays"]

        new_date = self.subtract_date(months=num_of_months, days=num_of_days)

        setting_dict["Date"] = new_date

    @classmethod
    def today_date(cls):
        """
        Get today's date.
        The method gets today's date and formats the date into a string. The reformatted date looks like: 24-Mar-2023
        :return: Returns the current day but reformatted into a string. (Ex. 24-Mar-2023)
        """
        today = date.today()
        return today.strftime("%d-%b-%Y")








