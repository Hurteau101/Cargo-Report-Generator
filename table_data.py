import pandas as pd
from datetime import date


class TableData:
    """
    A class for extracting data from an HTML table and setting values to be used in other classes.
    Class Utilizes the Panda Library.

      Attributes:
        - sla_data (dict) - SLA Data Dictionary
        - day_sorter (int): Day value that was used to filter the "Days" column.
        - highest_day (int): Highest value in the "Day" Column
        - home_delivery_awb_list (list): A list of AWB's.
        - shipped_awb_df (Dataframe): Shipped AWB's Dataframe
        - non_shipped_awb_df (Dataframe): Non-Shipped AWB's Dataframe
      Methods:
        - rename_columns: Rename columns in a Dataframe.
        - drop_columns: Drop columns in a Dataframe
        - insert_column: Insert columns in a Dataframe
        - convert_column_to_datatype: Convert columns to a specific type in a Dataframe
        - replace_column_str_values: Replace text in a column with another value in a Dataframe
        - rearrange_columns: Rearrange columns in a Dataframe
        - sort_columns: Sort columns in a Dataframe
        - drop_empty_values: Drop empty values in a Dataframe
        - create_report_data: Creates SLA/Bot or Home Delivery Report Data
        - get_sla_bot_data: Gets SLA Data Dictionary, Bot Data Dataframe and Highest Day Value
        - get_awb_list: Gets a list of AWB's and AWB information
        - get_home_delivery_data: Gets shipped AWB Dataframe and Non Shipped AWB Dataframe
    """

    # Valid Report constant which contains the report name and a tuple of the method name to be called along with the
    # instance attributes to be created at runtime.
    VALID_REPORTS = {
        "SLA/Bot Report": ("_create_bot_sla_table_data", ("sla_data", "day_sorter", "highest_day")),
        "Home Delivery Report": ("_create_home_delivery_data", ("home_delivery_awb_list", "shipped_awb_df",
                                                                "non_shipped_awb_df"))
    }

    def __init__(self, table_data: str, report_name: str):
        """
        Initializes a TableData object with the specified table data and report name.

        Upon initialization, the HTML table data is parsed using the `read_html` method
        of the pandas' library, and the resulting DataFrame is stored in the `table_df`
        attribute of the object. The `report_name` argument is used to determine which
        report to generate, and the appropriate method name and instance variables are
        retrieved from the `VALID_REPORTS` dictionary. The instance variables are then
        created and initialized to `None` using the `setattr` method.


        :param table_data: a string containing the HTML table data to be parsed
        :param report_name: The name of the report to be created. Must be one of the valid report names defined
            in VALID_REPORT.
        :raises KeyError: If the specified report name is not one of the valid report names defined in
            VALID_REPORT.
        """
        self.table_df = pd.read_html(table_data)[0]

        if report_name not in TableData.VALID_REPORTS.keys():
            raise KeyError(f"{report_name} is not a valid report. Valid reports are "
                           f"{' or '.join(TableData.VALID_REPORTS.keys())}")

        # create_report stores the tuple values for the method name to call.
        # instance_variables stores the tuple values to create the necessary instance variables.
        report_name, instance_variables = TableData.VALID_REPORTS[report_name]

        # Loop through the instance_variables assign them self, the variable name and the value none.
        for var in instance_variables:
            setattr(self, var, None)

    @staticmethod
    def rename_columns(dataframe: pd.DataFrame, column_names: dict) -> None:
        """
        Rename columns of a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_names: A dictionary of column names to be renamed. The keys are the old column names, the values
        are the new column names.
        """
        dataframe.rename(columns=column_names, inplace=True)

    @staticmethod
    def drop_columns(dataframe: pd.DataFrame, column_names: list) -> None:
        """
        Drops columns of a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_names: List of column names to drop.
        """
        dataframe.drop(columns=column_names, axis=1, inplace=True)

    @staticmethod
    def insert_column(dataframe: pd.DataFrame, column_name: str, last_column: bool = True,
                      column_position: int = None) -> pd.DataFrame:
        """
        Insert a column into a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_name: Column name to insert.
        :param last_column: Insert column at last position of Dataframe. (Default Value: True)
        :param column_position: Column position to insert the column. (Default Value: None)
        :return: Returns the modified Dataframe.
        :raise KeyError: Raises an error if last_column is set to False and no column position was set or if
            both last_column and column_position were set.
        """
        if not last_column and column_position is None:
            raise ValueError(f"last_column was set as {last_column} and no column position was set. Please"
                             f"insert a column position.")
        elif last_column and column_position is not None:
            raise ValueError("Both 'last_column' and 'column_position' cannot be set at the same time. "
                             "Please set only one.")

        if last_column:
            dataframe.insert(loc=len(dataframe.columns), column=column_name, value=" ")
            return dataframe
        else:
            dataframe.insert(column_position, column_name, value="")
            return dataframe

    @staticmethod
    def convert_column_to_datatype(dataframe: pd.DataFrame, column_name: str, data_type: str) -> pd.DataFrame:
        """
        Converts a column of one type to another type in a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_name: Column name to modify.
        :param data_type: Datatype to convert the column to. (Valid Types: 'int', 'float', 'str',
            'bool' or 'datetime64[ns]'
        :return: Returns the modified dataframe.
        :raise KeyError: Raises an error if data_type is not in the list of valid data types.
        """

        valid_data_types = ['int', 'float', 'str', 'bool', 'datetime64[ns]']
        if data_type not in valid_data_types:
            raise ValueError(f"{data_type} is not valid data type in this method")

        dataframe[column_name] = dataframe[column_name].astype(data_type)
        return dataframe

    @staticmethod
    def replace_column_str_values(dataframe: pd.DataFrame, column_name: str, string_value: str,
                                  replace_string_value: str) -> pd.DataFrame:
        """
        Replaces a column string value by removing part of the string in each row for that column.
        :param dataframe: Dataframe to modify.
        :param column_name: Column name to modify.
        :param string_value: The string to replace.
        :param replace_string_value: The string that replaces string_value
        :return: Returns the modified dataframe.
        """

        dataframe[column_name] = dataframe[column_name].str.replace(string_value, replace_string_value)
        return dataframe

    @staticmethod
    def rearrange_columns(dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
        """
        Re-arrange columns in a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_names: List of column names to rearrange. The order you pass in is the order the columns will
            display in the Dataframe.
        :return: Returns the modified dataframe.
        :raise KeyError: Raises an error if the column was not found in the Dataframe.
        """
        for column in column_names:
            if column not in dataframe.columns:
                raise KeyError(f"Column '{column}' not found in DataFrame")

        dataframe = dataframe.reindex(columns=column_names)
        return dataframe

    @staticmethod
    def sort_columns(dataframe: pd.DataFrame, column_name: str, ascending: bool) -> None:
        """
        Sorts a column in a Dataframe.
        :param dataframe: Dataframe to modify.
        :param column_name: Column name to sort.
        :param ascending: Sort by ascending.
        """
        dataframe.sort_values(by=column_name, ascending=ascending, inplace=True)

    @staticmethod
    def drop_empty_values(dataframe: pd.DataFrame, column_name: list) -> None:
        """
        Drops values that are empty in a list of columns.
        :param dataframe: Dataframe to modify.
        :param column_name: List of columns to check if the column contains any empty values.
        """
        dataframe.dropna(subset=column_name, inplace=True)

    @staticmethod
    def create_dataframe_copy(dataframe: pd.DataFrame) -> pd.DataFrame:
        """
        Create a dataframe copy.
        :param dataframe: Dataframe to copy.
        :return: Returns a copy of the Dataframe.
        """
        return dataframe.copy(deep=True)

    def create_report_data(self, report_name: str) -> None:
        """
        Executes the appropriate method call based on the report name. Either _create_bot_sla_table_data or
        _create_home_delivery_data will be executed.
        :param report_name: Name of the report to execute.
        :raise KeyError: If the specified report name is not one of the valid report names defined in
            VALID_REPORT.
        """
        if report_name not in TableData.VALID_REPORTS.keys():
            raise KeyError(f"{report_name} is not a valid report. Pass in the same Report Name as you did when you"
                           f" created the TableData Class. Valid reports are "
                           f"{' or '.join(TableData.VALID_REPORTS.keys())}")

        name_of_report = TableData.VALID_REPORTS[report_name][0]

        # Store the method object in report_method and then call that method based on the report_name passed in.
        report_method = getattr(self, name_of_report)
        report_method()

    def _sla_bot_starting_table_data(self) -> None:
        """
        Reformat the starting SLA/Bot Table.

        Reformat the SLA/Bot Table by dropping unnecessary columns and renaming columns/column values.
        """
        TableData.drop_columns(self.table_df, column_names=[0, 2, 3, 7, 8, 9, 13, 14])
        # Reset index, due to dropped columns.
        self.table_df = self.table_df.reset_index(drop=True)
        TableData.rename_columns(self.table_df, {
            1: "Route",
            4: "AWB",
            5: "Goods Desc.",
            6: "Cosignee",
            10: "Piece Count",
            11: "Weight",
            12: "Hours Remaining",
            15: "Recvd Date",
        })
        self.table_df = TableData.replace_column_str_values(dataframe=self.table_df, column_name="Route",
                                                            string_value="WPG = ", replace_string_value="")

    def get_sla_bot_data(self) -> tuple:
        """
        Get SLA/Bot Report Data.
        :return: Returns a tuple of SLA Data Dictionary, Bot Data Dataframe and Highest Day Value
        """
        return self.sla_data, self.table_df, self.highest_day

    def _create_bot_sla_table_data(self) -> None:
        """
        Creates the SLA/Bot Report Data
        """
        self._sla_bot_starting_table_data()
        self._create_sla_data()
        self._create_bot_data()

    def _create_bot_data(self) -> None:
        """
        Creates the Bot Table Data
        """
        self._reconfigure_bot_columns()
        self._add_day_values()
        self._sort_days()
        self._set_highest_day()
        TableData.sort_columns(dataframe=self.table_df, column_name="Days", ascending=False)
        self.table_df["Days"] = self.table_df["Days"] * -1

    def _reconfigure_bot_columns(self) -> None:
        """
        Reconfigure the Bot Table Data by sorting, dropping, inserting, etc.. columns.
        """
        TableData.drop_columns(dataframe=self.table_df, column_names=["Hours Remaining"])
        self.table_df.drop(self.table_df.index[0], inplace=True)
        TableData.drop_empty_values(dataframe=self.table_df, column_name=["Recvd Date"])
        # Reset index, due to dropped columns.
        self.table_df = self.table_df.reset_index(drop=True)

        self.table_df = TableData.insert_column(dataframe=self.table_df, last_column=True, column_name="Status")
        self.table_df = TableData.insert_column(dataframe=self.table_df, last_column=True, column_name="Remarks")
        self.table_df = TableData.insert_column(dataframe=self.table_df, last_column=False, column_name="Days",
                                                column_position=6)

        self.table_df = TableData.convert_column_to_datatype(dataframe=self.table_df, column_name="Piece Count",
                                                             data_type="int")

        # Convert the column to a float, incase there are float values.
        self.table_df = TableData.convert_column_to_datatype(dataframe=self.table_df, column_name="Weight",
                                                             data_type="float")
        # Round all values.
        self.table_df["Weight"] = self.table_df["Weight"].round()

        # Then convert to int, to avoid any errors if there are float values in column.
        self.table_df = TableData.convert_column_to_datatype(dataframe=self.table_df, column_name="Weight",
                                                             data_type="int")

    def _add_day_values(self) -> None:
        """
        Add values to the "Days" column.

        The method will loop through the "Recvd Date"
        column and take the "Recvd Date" value and subtract it with today's date. This will give us how many days
        a piece of cargo has been in the system. It will then input that new value into the "Days" column. The value
        will be negative, so we use Abs to convert it to a positive integer. Lastly drop the "Recvd" Column, as it
        won't be used anymore.
        """
        # Convert this column to a Timestamp object, to preform Datetime calculations.
        TableData.convert_column_to_datatype(dataframe=self.table_df, column_name="Recvd Date",
                                             data_type="datetime64[ns]")

        today_date = pd.Timestamp(date.today())

        for i in range(len(self.table_df["Recvd Date"])):
            delta = self.table_df.at[i, "Recvd Date"] - today_date
            # Added +1 to include today's date.
            self.table_df.at[i, "Days"] = abs(delta.days) + 1
        TableData.drop_columns(dataframe=self.table_df, column_names=["Recvd Date"])

    def _set_highest_day(self) -> None:
        """
        Set the highest value in the "Days" column. If empty, set to "N/A".
        """
        if len(self.table_df["Days"]) == 0:
            self.highest_day = "N/A"
        else:
            self.highest_day = self.table_df["Days"].max()

    def _sort_days(self) -> None:
        """
        Remove any rows that are less than the value of day_sorter.
        """

        self.table_df = self.table_df[self.table_df["Days"] >= self.day_sorter]

    def _create_sla_data(self) -> None:
        """
        Creates the SLA Table Data.
        """
        self._show_only_past_sla_rows()
        self._create_past_sla_dict()
        self._remove_common_destinations()
        self._sort_sla_dictionary()

    def _show_only_past_sla_rows(self) -> None:
        """
        Drop all rows in the "Hours Remaining" column that do NOT contain "-".
        """
        self.sla_data = self.table_df.drop(self.table_df[~self.table_df["Hours Remaining"].str.contains('-')].index)

    def _create_past_sla_dict(self) -> None:
        """
        Replaces dataframe to an SLA dictionary grouped by the "Route" column.

        Method uses the group method to group all the "Route" values and then sums up all the "Weight" values that
        are associated with that "Route" into a dictionary.
        """
        TableData.convert_column_to_datatype(dataframe=self.sla_data, column_name="Weight", data_type="int")
        self.sla_data = self.sla_data.groupby('Route')['Weight'].sum().to_dict()

    def _sort_sla_dictionary(self) -> None:
        """
        Sort SLA dictionary by the destination with the highest number.
        """
        self.sla_data = dict(sorted(self.sla_data.items(), key=lambda x: x[1], reverse=True))

    def _remove_common_destinations(self) -> None:
        """
        Add common destination locations together in the SLA Dictionary.

        This method checks to see if any destination has a common destination in the SLA dictionary. If there are
        common destinations, it will combine it into 1 main key/value in the SLA dictionary with all values being added
        up.
        """

        st_theresa_common_destinations = ["YST", "WGK"]
        thompson_common_destinations = ["ZAC", "XLB", "YTH", "XTL", "YBT", "XSI"]

        if any(destination in self.sla_data for destination in thompson_common_destinations):
            yth_location_sum = sum(self.sla_data[destination] and self.sla_data.pop(destination) for
                                   destination in thompson_common_destinations if destination in self.sla_data)
            self.sla_data["YTH Locations"] = yth_location_sum

        if any(destination in self.sla_data for destination in st_theresa_common_destinations):
            st_theresa_location_sum = sum(self.sla_data[destination] and self.sla_data.pop(destination)
                                          for destination in st_theresa_common_destinations if
                                          destination in self.sla_data)
            self.sla_data["YST/WGK Locations"] = st_theresa_location_sum

    def get_awb_list(self) -> list:
        """
        Gets a list of AWB's and AWB information and stores them in a list of dictionary's.

        :return: Returns a list of AWB Dictionary's.
        """
        self.table_df = TableData.replace_column_str_values(dataframe=self.table_df, column_name="Consignment #",
                                                            string_value="632-",
                                                            replace_string_value="")

        records = self.table_df.to_dict(orient="records")

        awb_list = [{"AWB No.": record["Consignment #"], "Consignee": record["Consignee Name"].title(),
                     "Community": record["To"], "No. of Pieces": record["Pieces"]} for record in records]
        return awb_list

    def _sort_home_delivery_awbs(self) -> None:
        """
        Create 2 Dataframes for Shipped AWB's and Non-Shipped AWB's.

        This will create 2 Dataframes based on checking if an AWB has been shipped or not.
        """
        # Use .copy() as you are not modifying the original data frame. You are filtering through the column
        # and creating a new dataframe for shipped_awb_data and not_shipped_awb_data
        self.shipped_awb_df = self.table_df[self.table_df["Flight Status"].str.contains("Allocated")].copy()
        self.non_shipped_awb_df = self.table_df[~self.table_df["Flight Status"].str.contains("Allocated")].copy()

    def _format_home_delivery_dataframe(self) -> None:
        """
        Responsible for reformatting the Shipped AWB Dataframe and Non-Shipped AWB Dataframe.
        """
        self._sort_home_delivery_awbs()

        TableData.drop_columns(dataframe=self.shipped_awb_df, column_names=["Flight Status"])
        TableData.drop_columns(dataframe=self.non_shipped_awb_df, column_names=["Consignee", "Flight Number",
                                                                                "Flight Date", "No. of Pieces"])
        self.shipped_awb_df["Flight Number"] = self.shipped_awb_df["Flight Number"].str.upper()
        TableData.sort_columns(dataframe=self.shipped_awb_df, column_name="Flight Date", ascending=False)

        # Use apply method on the AWB No. Column. The apply method calls a function on the column (AWB No.)
        # We use lambda as the function call to store the current value in x and add 632- to it.
        self.shipped_awb_df["AWB No."] = self.shipped_awb_df["AWB No."].apply(lambda x: f"632-{x}")
        self.non_shipped_awb_df["AWB No."] = self.non_shipped_awb_df["AWB No."].apply(lambda x: f"632-{x}")

        TableData.rename_columns(dataframe=self.shipped_awb_df, column_names={"Flight Number": "Flight No.",
                                                                              "Flight Date": "Date"})

        self.shipped_awb_df = TableData.rearrange_columns(dataframe=self.shipped_awb_df,
                                                          column_names=["Date", "Flight No.", "Community",
                                                                        "AWB No.", "No. of Pieces",
                                                                        "Consignee"])

    def _create_home_delivery_data(self) -> None:
        """
        Creates the Home Delivery Data.
        """
        self.table_df = pd.DataFrame(self.home_delivery_awb_list)
        self._format_home_delivery_dataframe()

    def get_home_delivery_data(self) -> tuple:
        """
        Get Home Delivery Report Data.
        :return: Returns a tuple of Shipped AWB Dataframe and Non Shipped AWB Dataframe
        """
        return self.shipped_awb_df, self.non_shipped_awb_df
