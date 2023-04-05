from Database_Connector import DatabaseConnector
from utils import type_check


class SettingsData:
    """
    A class for updating and reading all Setting Values to and from the Database.

     Attributes:
        - connector -  An instance of the DatabaseConnector class that is used to connect to and interact
            with a database

     Methods:
        - get_bot_sla_data: Returns the SLA/Bot Report Setting values that were retrieved from the database.
        - get_home_delivery_data: Returns the Home Delivery Setting values that were retrieved from the database.
        - get_setting_data: Gets all the data from a table in the database and stores it in a dictionary.
        - update_database: Updates the current SLA/Bot Setting Values and/or the current Home
          Delivery Setting values to the database.
    """

    BOT_SLA_REPORT_TABLE_NAME = "BotReportSettings"
    HOME_REPORT_TABLE_NAME = "HomeReportSettings"

    def __init__(self):
        """
         Initializes a SettingsData Object.

         Creates a new instance of the DatabaseConnector class and assigns it to the `connector` attribute
        """

        self.connector = DatabaseConnector()

    def get_bot_sla_data(self) -> dict:
        """
        Gets all the values from the Bot/SLA table in the database.

        This method gets all the values from the SLA/Bot table in the database. The values are all the previously
        stored setting values for the SLA/Bot Settings. It returns it as a dictionary where the keys are the
        column names and the values are the values for that column.

        :return: Returns a dictionary of values for the SLA/Bot settings.
        """
        return self.get_setting_data(self.BOT_SLA_REPORT_TABLE_NAME)

    def get_home_delivery_data(self) -> dict:
        """
       Gets all the values from the Home Delivery table in the database.

       This method gets all the values from the Home Delivery table in the database. The values are all the previously
       stored setting values for the Home Delivery Settings. It returns it as a dictionary where the keys are the
       column names and the values are the values for that column.

       :return: Returns a dictionary of values for the SLA/Bot settings.
       """
        return self.get_setting_data(self.HOME_REPORT_TABLE_NAME)

    def get_setting_data(self, table_name: str) -> dict:
        """
        Gets all the specified table data and returns the table data as a dictionary

        This method accepted a table_name as an argument which will then look into the database for that table. It will
        then retire all the columns and row for that table and store it as a dictionary where the keys are the
        column names and the values are the values for that column. The method also calls "type_check" which ensures
        that the table name is a string, if it's not it will raise an exception. The method also ensures that
        the table name provided is a table name that should be expected, otherwise it will raise an exception.

        :param table_name: The name of the table to retrieve data from. Valid values are
        "BotReportSettings and HomeReportSettings
        :return Returns a dictionary of values for the specified table.
        :raise TypeError: Will raise an error if the table name is not of type string or will raise ValueError if
                you try to update a table that is not in the Database. Valid table names
                (BotReportSettings or HomeReportSettings)
        """
        type_check(arg=table_name, arg_name="table_name", expected_type=str)

        valid_tables = [self.HOME_REPORT_TABLE_NAME, self.BOT_SLA_REPORT_TABLE_NAME]

        if table_name not in valid_tables:
            raise ValueError(f"{table_name} is an invalid table name. Please only update the 2 "
                             f"tables provided {self.BOT_SLA_REPORT_TABLE_NAME} or {self.HOME_REPORT_TABLE_NAME}")

        self.connector.connect()
        cursor = self.connector.connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        row = cursor.fetchone()

        column_names = [column_name[0] for column_name in cursor.description]
        settings_data = {column_names[i]: row[i] for i in range(len(column_names))}

        self.connector.close_conn()

        return settings_data

    def update_database(self, table_name: str, **kwargs) -> None:
        """
        This will update the setting values for the specified table in the database.
        This method will take a table_name as an argument and update the kwarg values in the setting window
        to the specified table in the database. The method will also ensure the proper types are inputted for
        the **kwargs, or it will raise an exception.

        Args:
            - table_name: The database table name that you want to update.
            - **kwargs: Additional keyword arguments that can be passed to the function (required).

        Keyword Args:
            - DayAmount(int) - The Entry Box value for "Days"
            - NumOfMonths(int) - The Entry Box value for "Number of Months Back"
            - NumOfDays(int) - The Entry Box value for "Number of Days Back"
            - FromAirport(str) - The Entry Box value for "From Airport"
            - ToAirport(str) - The Entry Box value for "To Airport"
            - Keyword(str) - The Entry Box value for "Keyword"

        :raise ValueError: Will raise error if the table is not in the Database.
        """
        day_amount = kwargs.get("DayAmount")
        num_of_months = kwargs.get("NumOfMonths")
        num_of_days = kwargs.get("NumOfDays")
        from_airport = kwargs.get("FromAirport")
        to_airport = kwargs.get("ToAirport")
        keywords = kwargs.get("Keyword")

        expected_types = {
            "DayAmount": int,
            "NumOfMonths": int,
            "NumOfDays": int,
            "FromAirport": str,
            "ToAirport": str,
            "Keyword": str
        }

        for key, expected_type in expected_types.items():
            if key in kwargs:
                type_check(arg=kwargs[key], arg_name=key, expected_type=expected_type)

        valid_table_names = [self.HOME_REPORT_TABLE_NAME, self.BOT_SLA_REPORT_TABLE_NAME]

        if table_name in valid_table_names:
            self.connector.connect()
            cursor = self.connector.connection.cursor()

            if table_name == self.BOT_SLA_REPORT_TABLE_NAME:
                cursor.execute(f"UPDATE {table_name} SET DayAmount = ?, NumOfMonths = ?, "
                               f"NumOfDays = ?, FromAirport = ?, ToAirport = ?;",
                               (day_amount, num_of_months, num_of_days, from_airport, to_airport))
            elif table_name == self.HOME_REPORT_TABLE_NAME:
                cursor.execute(f"UPDATE {table_name} SET Keyword = ?, NumOfMonths = ?, "
                               f"NumOfDays = ?, FromAirport = ?, ToAirport = ?;",
                               (keywords, num_of_months, num_of_days, from_airport, to_airport))
            self.connector.connection.commit()
            self.connector.close_conn()
        else:
            raise ValueError(f"{table_name} is an invalid table name. Please only update the 2 "
                             f"tables provided {self.BOT_SLA_REPORT_TABLE_NAME} or {self.HOME_REPORT_TABLE_NAME}")
