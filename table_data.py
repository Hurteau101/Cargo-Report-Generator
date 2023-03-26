import pandas as pd


class TableData:
    def __init__(self, waybill_table):
        # TODO: Uncomment once ready to test fully.
        self.table_data = pd.read_html(waybill_table)[0]
        #self.table_data = waybill_table
        self.sla_data = None

    @classmethod
    def export_to_excel(cls, dataframe: pd.DataFrame, excel_name: str):
        """
        Export the Dataframe to an Excel File.
        :param dataframe: The Dataframe you want to export to an Excel File
        :param excel_name: Pass in the name you want your Excel file to be.
        :return: None
        """
        # index = False so the index will not be included in the Excel file.
        with pd.ExcelWriter(excel_name) as writer:
            dataframe.to_excel(writer, index=False)

    @classmethod
    def rename_columns(cls, dataframe: pd.DataFrame, column_names: dict) -> pd.DataFrame:
        """
        Renames the specified columns.
        This method takes a dictionary of Column names. The key is the old column names and value is the
        new column names
        :param dataframe: The DataFrame to modify.
        :param column_names: Dictionary of column names. Key = old column names : Values = new column names
        :return: Returns the new modified DataFrame with the column name changes.
        """
        dataframe.rename(columns=column_names, inplace=True)
        return dataframe

    @classmethod
    def drop_columns(cls, dataframe: pd.DataFrame, column_names: list) -> pd.DataFrame:
        """
        Drops the specified columns that are passed in as column_name agreement.
        This method takes a list of column names that you want to delete from the DataFrame.
        :param dataframe: The DataFrame to modify.
        :param column_names: The list of Columns to delete.
        :return: Returns the new modified DataFrame with the specific columns deleted.
        """
        dataframe.drop(column_names, axis=1, inplace=True)
        return dataframe

    @classmethod
    def insert_column(cls, dataframe: pd.DataFrame, last_column: bool, column_name: str,
                      column_position: int = None) -> pd.DataFrame:
        """
        Insert columns into the DataFrame.
        This method allows you to insert a column at a specific position or at the end of the last column. If
        last_column = False, ensure you pass in the column_position as an int of where you want to insert the column.
        :param dataframe: The DataFrame to modify.
        :param last_column: Select if you want the column to be inserted at the end. True = Column inserted at the end,
        False  = Column inserted at your desired position by specifying the column_position argument.
        :param column_name: Name of the column to insert.
        :param column_position: What position to insert the column.
        :return: Returns the new modified DataFrame with the newly inserted column.
        """
        if not last_column and column_position is None:
            raise ValueError("If last_column is False, please select a position to insert the column with "
                             "column_position argument. Must be an int!")

        if last_column:
            dataframe.insert(loc=len(dataframe.columns), column=column_name, value=" ")
            return dataframe
        else:
            dataframe.insert(column_position, column_name, value="")
            return dataframe

    def reformat_sla_bot_table(self):
        """
        Reformat the DataFrame to ensure the appropriate columns are displayed, the appropriate column names and to
        ensure only the necessary rows are displayed for the SLA/Bot Report.
        :return: None
        """
        self.drop_columns(self.table_data, [0, 2, 3, 7, 8, 9, 13, 14])
        self.rename_columns(self.table_data, {
            1: "Route",
            4: "AWB",
            5: "Goods Desc.",
            6: "Cosignee",
            10: "Peice Count",
            11: "Weight",
            12: "Days",
            15: "Recvd Date"
        })

        self.table_data = self.insert_column(self.table_data, last_column=True, column_name="Status")
        self.table_data = self.insert_column(self.table_data, last_column=True, column_name="Remarks")
        self.table_data = self.modify_column_string(self.table_data, column_name="Route", replace_string="WPG = ",
                                                    replace_string_with="")
        self.get_past_sla_rows()

    def get_past_sla_rows(self):
        """
        Deletes any row in the DataFrame that contains "-" in the Days Column. This is to ensure that only past
        SLA rows are shown.
        :return: None
        """
        # Check if "-" in column 12. If "-" in column 12, return true. Returns all rows with "-"
        # ~ is used to invert the boolean value that is returned from this. Without the ~ it would only display
        # rows that don't contain "-". We only want to display values with "-".
        self.table_data.drop(self.table_data[~self.table_data["Days"].str.contains('-')].index,
                             inplace=True)

    @classmethod
    def modify_column_string(cls, dataframe: pd.DataFrame, column_name: str, replace_string: str,
                             replace_string_with: str) -> pd.DataFrame:
        """
        Modify the text in the rows. Remove any part of a string in that row to a new value.
        (Ex. Old String: "WPG = YYC". Using this method - (YYC). It removed "WPG = " from that specific value.
        :param dataframe: The DataFrame to modify.
        :param column_name: The column to check which rows to modify.
        :param replace_string: Replaces the string specified (Can be full string or part of string).
        :param replace_string_with: Replace with this string.
        :return: Returns the new modified DataFrame with the newly modified string(s).
        """
        dataframe[column_name] = dataframe[column_name].str.replace(replace_string, replace_string_with)
        return dataframe

    @classmethod
    def convert_column_to_int(cls, dataframe: pd.DataFrame, column_name: str) -> pd.DataFrame:
        """
        Converts an entire column to int datatype.
        :param dataframe: The DataFrame to modify.
        :param column_name: The column to convert to an int.
        :return: Returns the new modified DataFrame with the column converted to an integer.
        """
        dataframe[column_name] = dataframe[column_name].astype('int')
        return dataframe

    def get_past_sla_data(self, dataframe: pd.DataFrame):
        """
        Store all the values in the "Route" column into a dictionary with the name of the "Route" being the key and then
        adding all the weight values that are associated with that route for the value key. Method uses the group
        method to group all the "Route" values and then sums up all the "Weight" values that are associated with that
        "Route" into a dictionary.
        :param dataframe: The DataFrame to modify.
        :return:
        """
        self.convert_column_to_int(dataframe, "Weight")
        self.sla_data = dataframe.groupby('Route')['Weight'].sum().to_dict()

    def reformat_past_sla_data(self, dataframe: pd.DataFrame):
        """
        Creates the SLA Dictionary and reformat it to display in the proper way. It first calls the get_sla_data,
        which gets the SLA dictionary and stores it in the sla_data attribute. It then adds all common destinations into
        the sla_data dictionary. Lastly it will sort the sla_data dictionary by highest value first.
        :param dataframe: The DataFrame to modify.
        :return: None
        """
        self.get_past_sla_data(dataframe)
        self.add_common_destinations()
        self.sort_dictionary()

    def add_common_destinations(self):
        """
        Add Common Destination Locations together. There are 2 main destinations that have common alternate
        destinations: YST/WGK Locations - YST and WGK | YTH Locations - ZAC, XLB, YTH, XTL, YBT and XSI

        This method checks to see if any of those alternate destinations are in the sla_data dictionary. If they are,
        it will add up and combine all those alternate dictionaries and combine it into 1 main key dictionary with
        all the alternate destination values added up.

        :return: None
        """
        st_theresa_common = ["YST", "WGK"]
        thompson_common = ["ZAC", "XLB", "YTH", "XTL", "YBT", "XSI"]

        if any(destination in self.sla_data for destination in thompson_common):
            yth_location_sum = sum(self.sla_data[destination] and self.sla_data.pop(destination) for
                                   destination in thompson_common if destination in self.sla_data)
            self.sla_data["YTH Locations"] = yth_location_sum

        if any(destination in self.sla_data for destination in st_theresa_common):
            st_theresa_location_sum = sum(self.sla_data[destination] and self.sla_data.pop(destination)
                                         for destination in st_theresa_common if destination in self.sla_data)
            self.sla_data["YST/WGK Locations"] = st_theresa_location_sum

    def sort_dictionary(self):
        """
        Sort SLA Data Dictionary by the destination with the highest number.
        :return: None
        """
        # Sort dictionary in reverse order (The Highest value first). Since sorted will return a
        # tuple, we use dict to convert it back to a dictionary. x[1] so we start at index 1 which is the values
        # the keys would be [0]
        self.sla_data = dict(sorted(self.sla_data.items(), key=lambda x: x[1], reverse=True))
