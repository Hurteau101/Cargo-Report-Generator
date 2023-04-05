from dateutil.relativedelta import relativedelta
from datetime import date
from dotenv import load_dotenv
import os
from Settings_Data import SettingsData


class WebpageData:
    """
    This class is used to obtain all necessary data for the Cargo Webpage. Such as links,
    saved settings, user info, etc.

     Attributes:
        - _username (private) - The username. (Use get_username to access)
        - _password (private) - The password (Use get_password to access)
        - _cargo_homepage (private) - The Cargo Homepage URL (Use get_cargo_homepage to access)
        - _waybill_url (private) - The Waybills to Ship URL (Use get_waybill_url to access)
        - _search_awb_url (private) - The search AWB URL (Use get_search_awb_url to access)
     Methods:
         - get_username: Get the username.
         - get_password: Get the password.
         - get_cargo_homepage: Get the Cargo homepage URL.
         - get_waybill_url: Get the Waybills to Ship URL.
         - get_search_awb_url: Get the Search AWB URL.
         - subtract_date: Subtract a date.
         - get_setting_values: Get setting values from the Database.
    """

    load_dotenv()
    USERNAME = os.getenv("USERNAME_1")
    PASSWORD = os.getenv("PASSWORD")
    CARGO_HOMEPAGE = os.getenv("CARGO_HOMEPAGE")
    WAYBILLS_REPORT_URL = os.getenv("WAYBILLS_REPORT_URL")
    SEARCH_AWB_URL = os.getenv("SEARCH_AWB_URL")

    def __init__(self):
        """
        Initializes a WebpageData Object.

        Sets up the instance with the necessary attributes for accessing
        and interacting with the Cargo Webpage. It sets the username, password, and URLs for the Cargo homepage,
        Waybills Report page, and Search AWB page
        """
        self._username = WebpageData.USERNAME
        self._password = WebpageData.PASSWORD
        self._cargo_homepage = WebpageData.CARGO_HOMEPAGE
        self._waybill_url = WebpageData.WAYBILLS_REPORT_URL
        self._search_awb_url = WebpageData.SEARCH_AWB_URL

    def get_username(self) -> str:
        """
        Get username.
        :return: Returns the username.
        """
        return self._username

    def get_password(self) -> str:
        """
        Get password
        :return: Returns the password
        """
        return self._password

    def get_cargo_homepage(self) -> str:
        """
        Gets the Cargo Homepage URL
        :return: Returns the Cargo Homepage URL
        """
        return self._cargo_homepage

    def get_waybill_url(self) -> str:
        """
        Gets the Waybills to Ship URL
        :return: Returns the Waybills to Ship URL
        """
        return self._waybill_url

    def get_search_awb_url(self) -> str:
        """
        Get the Search AWB URL
        :return: Returns the Search AWB URL
        """
        return self._search_awb_url

    @staticmethod
    def subtract_date(months: int = 0, days: int = 0) -> str:
        """
        Subtracts the current date by the amount of months set and days set.

        :param months: Amount of months you want to subtract from the current date. (Default: 0)
        :param days: Amount of days you want to subtract from the current date. (Default: 0)
        :return: Returns the date as a reformatted string. (Ex. 25-Mar-2023)
        """
        today_date = date.today()
        new_date_object = today_date + relativedelta(months=-months, days=-days)
        new_date_string = new_date_object.strftime('%d-%b-%Y')

        return new_date_string

    @staticmethod
    def get_setting_values(setting_group: str) -> dict:
        """
        Get the settings values for a specific setting group.

        This method will get the setting values which are stored in a database. It will obtain the values based on
        the setting group of "SLA" or "Home" It will also update the dictionary to add a
        new item of 'Date' to the dictionary to be used to fill in dates on the Cargo Webpage.

        :param setting_group: Setting group you want to get. (Valid Options: "SLA/Bot" or "Home").
        :return: Returns a dictionary of the settings.
        :raise ValueError: Will raise error if the correct setting group is not passed in. Valid Settings Groups:
            'SLA' or 'Home'.
        """

        settings = SettingsData()

        if setting_group.upper() == "SLA":
            sla_dict = settings.get_bot_sla_data()
            WebpageData._update_setting_dictionary(sla_dict)
            return sla_dict
        elif setting_group.upper() == "HOME":
            home_dict = settings.get_home_delivery_data()
            WebpageData._update_setting_dictionary(home_dict)
            return home_dict
        else:
            raise ValueError(f"{setting_group} is not a valid setting group. Please only pass in 'SLA' or 'Home'")

    @classmethod
    def _update_setting_dictionary(cls, setting_dict) -> None:
        """
        Updates the appropriate settings to prevent errors on the script.

        This method updates any dictionary that needs to be updated with specific values, so that when the dictionary
        is called later on to fill in a form, no value errors are provided by selenium. Method updates the date settings
        and airport settings.

        :param setting_dict: Pass in which setting dictionary to update. Should be either SLA/Bot Report Setting or
        Home Delivery Setting Dictionary
        """
        WebpageData._update_date_settings(setting_dict)
        WebpageData._update_airport_dictionary(setting_dict)

    @classmethod
    def _update_airport_dictionary(cls, setting_dict: dict) -> None:
        """
        Checks the dictionary key of "ToAirport" and "FromAirport" to see if the value is "Please Select". If it is
        it updates its value to 0.

        This method checks to see if the dictionary key of the passed in setting dictionary for "ToAirport" and
        "FromAirport" values are "Please Select". If they are, they will be changed to 0. The reason for this, is the
        drop-down for each of the airport's "Please Select" value isn't actually "Please Select". The value is
        associated with 0 instead. This will prevent errors of not finding that value.

        :param setting_dict: Pass in which setting dictionary to update. Should be either SLA/Bot Report Setting or
        Home Delivery Setting Dictionary.
        """
        to_airport = setting_dict["ToAirport"]

        if to_airport == "Please Select":
            setting_dict["ToAirport"] = "0"

    @classmethod
    def _update_date_settings(cls, setting_dict: dict) -> None:
        """
        Add a configured date to the specific setting_dict. (Ex. Date: 25-Mar-2023 added to dictionary)

        This method will add a new date string to the specified dictionary. This new date will be used on the Cargo
        Webpage that requires you to fill in dates. We are using the settings of NumOfMonths which is used to
        decide how many months back to go from the current date and NumOfDays which is used to decide how many days
        to go back from the current date. Using that information, this method can create a date item in the dictionary.

        :param setting_dict: Pass in the appropriate setting dictionary. Valid values are sla_bot_setting_data or
            sla_bot_setting_data dictionary attribute.
        """
        num_of_months = setting_dict["NumOfMonths"]
        num_of_days = setting_dict["NumOfDays"]

        new_date = WebpageData.subtract_date(months=num_of_months, days=num_of_days)

        setting_dict["Date"] = new_date

