from Database_Connector import DatabaseConnector
from utils import type_check


class SettingsData:
    BOT_SLA_REPORT_TABLE_NAME = "BotReportSettings"
    HOME_REPORT_TABLE_NAME = "HomeReportSettings"

    def __init__(self):
        self.connector = DatabaseConnector()

    def get_bot_sla_data(self):
        return self.get_setting_data(self.BOT_SLA_REPORT_TABLE_NAME)

    def get_home_delivery_data(self):
        return self.get_setting_data(self.HOME_REPORT_TABLE_NAME)

    def get_setting_data(self, table_name: str):
        """
        Returns the table data as a dictionary

        :param table_name: The name of the table to retrieve data from. Valid values are
        "BotReportSettings and HomeReportSettings
        """
        type_check(arg=table_name, arg_name="table_name", expected_type=str)

        valid_tables = [self.HOME_REPORT_TABLE_NAME, self.BOT_SLA_REPORT_TABLE_NAME]

        if table_name not in valid_tables:
            raise ValueError(f"{table_name} is not a valid table in the database")

        self.connector.connect()
        cursor = self.connector.connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        row = cursor.fetchone()

        column_names = [column_name[0] for column_name in cursor.description]
        settings_data = {column_names[i]: row[i] for i in range(len(column_names))}

        return settings_data

    # TODO: Add doctsring
    def update_sla_bot_settings(self, table_name: str, **kwargs):
        day_amount = kwargs.get("DayAmount")
        num_of_months = kwargs.get("NumOfMonths")
        num_of_days = kwargs.get("NumOfDays")
        from_airport = kwargs.get("FromAirport")
        to_airport = kwargs.get("ToAirport")

        self.connector.connect()
        cursor = self.connector.connection.cursor()
        cursor.execute(f"UPDATE {table_name} SET DayAmount = ?, NumOfMonths = ?, "
                       f"NumOfDays = ?, FromAirport = ?, ToAirport = ?;",
                       (day_amount, num_of_months, num_of_days, from_airport, to_airport))
        self.connector.connection.commit()

    # TODO: Add doctsring
    def update_home_settings(self, table_name: str, **kwargs):
        keywords = kwargs.get("Keyword")
        num_of_months = kwargs.get("NumOfMonths")
        num_of_days = kwargs.get("NumOfDays")
        from_airport = kwargs.get("FromAirport")
        to_airport = kwargs.get("ToAirport")

        self.connector.connect()
        cursor = self.connector.connection.cursor()
        cursor.execute(f"UPDATE {table_name} SET Keyword = ?, NumOfMonths = ?, "
                       f"NumOfDays = ?, FromAirport = ?, ToAirport = ?;",
                       (keywords, num_of_months, num_of_days, from_airport, to_airport))
        self.connector.connection.commit()


