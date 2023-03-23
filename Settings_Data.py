from Database_Connector import DatabaseConnector
from utils import type_check


class SettingsData:
    def __init__(self):
        self.connector = DatabaseConnector()

    def get_bot_sla_data(self):
        return self.get_setting_data("BotReportSettings")

    def get_home_delivery_data(self):
        return self.get_setting_data("HomeReportSettings")

    def get_setting_data(self, table_name: str):
        """
        Returns the table data as a dictionary

        :param table_name: The name of the table to retrieve data from. Valid values are
        "BotReportSettings and HomeReportSettings
        """
        type_check(arg=table_name, arg_name="table_name", expected_type=str)

        valid_tables = ["BotReportSettings", "HomeReportSettings"]

        if table_name not in valid_tables:
            raise ValueError(f"{table_name} is not a valid table in the database")

        self.connector.connect()
        cursor = self.connector.connection.cursor()

        cursor.execute(f"SELECT * FROM {table_name}")
        row = cursor.fetchone()

        column_names = [column_name[0] for column_name in cursor.description]
        settings_data = {column_names[i]: row[i] for i in range(len(column_names))}

        return settings_data
