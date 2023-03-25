from dateutil.relativedelta import relativedelta
from datetime import date
from dotenv import load_dotenv
import os

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
        self.home_setting_data = None
        self.sla_bot_setting_data = None


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
        new_date_object = today_date + relativedelta(months=months, days=days)
        new_date_string = new_date_object.strftime('%d-%b-%Y')

        return new_date_string

    def get_setting_values(self, settings_data: object):
        """
        Gets the setting values that are stored in the database and sets them to the appropriate attributes.
        This method will get the setting values which are stored in a database. These values will be used later on
        to fill in a webpage form to generate the appropriate reports.
        :param settings_data: Pass in the SettingData() class which holds a method to retrieve the appropriate settings
        for either the SLA/Bot Settings or Home Delivery Settings
        :return: None
        """
        self.sla_bot_setting_data = settings_data.get_bot_sla_data()
        self.home_setting_data = settings_data.get_home_delivery_data()

    def update_date_settings(self):
        pass

    def test(self):
        setting_data = SettingsData()
        self.get_setting_values(setting_data)

        print(self.home_setting_data)
        print(self.sla_bot_setting_data)


    @classmethod
    def today_date(cls):
        """
        Get today's date.
        The method gets today's date and formats the date into a string. The reformatted date looks like: 24-Mar-2023
        :return: Returns the current day but reformatted into a string. (Ex. 24-Mar-2023)
        """
        today = date.today()
        return today.strftime("%d-%b-%Y")












 # @property
    # def username(self) -> str:
    #     """
    #     Get the username
    #     :return: Returns the username.
    #     """
    #     return self._username
    #
    # @username.setter
    # def username(self, username: str):
    #     """
    #     Set username
    #     :param username: The username for the cargo webpage.
    #     :return: None
    #     """
    #     self._username = username
    #
    # @property
    # def password(self) -> str:
    #     """
    #     Get the password
    #     :return: Returns the password
    #     """
    #     return self._password
    #
    # @password.setter
    # def password(self, password: str):
    #     """
    #     Set password
    #     :param password:  The password for the cargo webpage.
    #     :return: None
    #     """
    #     self._password = password