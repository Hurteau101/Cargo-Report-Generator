import pandas as pd
from datetime import date


class TableData:
    """
        A class for extracting data from an HTML table and setting values to be used in other classes.
        Class Utilizes the Panda Library.

       Main Attributes:
           - table_data - The main table. Reads an HTML table that is passed in via the constructor.
           - sla_data - All data that is related to the SLA Table portion

       Main Operations:
           - create_starting_table - Creates the main table data and updates it by dropping necessary columns, renaming
           columns, and dropping necessary text.
           - sla_report_creation_data - Calls all methods that are responsible for creating the SLA Report Data.
           - bot_report_creation_data - Calls all methods that are responsible for creating the Bot Report Data.
       """

    def __init__(self, waybill_table):
        # TODO: Uncomment once ready to test fully.
        #self.table_data = waybill_table
        self.table_data = pd.read_html(waybill_table)[0]
        self.sla_data = None
        # This attribute is used to filter the rows by a certain day.
        self.day_sorter = 0
        self.sla_weight_sum = 0
        self.highest_day = 0
        self.shipped_awb_data = None
        self.not_shipped_awb_data = None

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
    def drop_columns(cls, dataframe: pd.DataFrame, column_names: list):
        """
        Drops the specified columns that are passed in as column_name agreement.
        This method takes a list of column names that you want to delete from the DataFrame.
        :param dataframe: The DataFrame to modify.
        :param column_names: The list of Columns to delete.
        :return: None
        """
        dataframe.drop(column_names, axis=1, inplace=True)

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

    @classmethod
    def convert_column_to_datatype(cls, dataframe: pd.DataFrame, column_name: str, data_type: str) -> pd.DataFrame:
        """
        Converts an entire column to a specified data type.

        :param dataframe: The DataFrame to modify.
        :param column_name: The column to convert to an int.
        :param data_type: The datatype to convert the column to. (Valid Types: 'int', 'float', 'str',
        'bool', 'datetime64[ns]'
        :return: Returns the new modified DataFrame with the column converted to an integer.
        """

        valid_data_types = ['int', 'float', 'str', 'bool', 'datetime64[ns]']
        if data_type not in valid_data_types:
            raise ValueError(f"{data_type} is not valid data type in this method")

        dataframe[column_name] = dataframe[column_name].astype(data_type)
        return dataframe

    @classmethod
    def _rearrange_columns(cls, dataframe: pd.DataFrame, rearrange_column_names: list):
        """
        Re-arranges the way the columns are ordered. Ex (AWB, Date, Notes) - rearrange_column_names = [Date, Notes, AWB]
        The dataframe will now display the columns as Date, Notes, AWB.
        :param dataframe: The DataFrame to modify.
        :param rearrange_column_names: List of the new re-arranged column names.
        :return: Returns the modified dataframe with the re-arranged columns.
        """
        dataframe = dataframe.reindex(columns=rearrange_column_names)
        return dataframe

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
    def sort_column(cls, dataframe: pd.DataFrame, column_name: str, ascending: bool):
        """
        Sort a dataframe column based on its values.
        :param dataframe: The DataFrame to modify.
        :param column_name: Name of the column to sort.
        :param ascending: Sort in ascending. True = ascending order | False = descending order
        :return: None
        """
        dataframe.sort_values(by=column_name, ascending=ascending, inplace=True)

    def create_starting_table(self):
        """
        Reformat the SLA/Bot Report starting table data, by dropping unnecessary columns, renaming the header rows and
        removing any value in the "Route" column that starts with "WPG = ".
        :return: None
        """
        self.drop_columns(dataframe=self.table_data, column_names=[0, 2, 3, 7, 8, 9, 13, 14])
        # Reset index, due to dropped columns.
        self.table_data = self.table_data.reset_index(drop=True)
        self.rename_columns(self.table_data, {
            1: "Route",
            4: "AWB",
            5: "Goods Desc.",
            6: "Cosignee",
            10: "Piece Count",
            11: "Weight",
            12: "Hours Remaining",
            15: "Recvd Date",
        })

        self.table_data = self.modify_column_string(self.table_data, column_name="Route", replace_string="WPG = ",
                                                    replace_string_with="")

    def sla_report_creation_data(self):
        """
        Calls all methods that are responsible for creating the SLA Report Data. Such methods are getting only
        keeping the rows that are in the negatives in "Hours Remaining" column (get_past_sla_rows),
        grouping together all common alternative destinations (add_common_destinations), sorting the SLA dictionary
        to show the highest value first (sort_dictionary) and lastly adding up all the sla_data values to get a total
        weight.
        :return: None
        """
        sla_dataframe = self._get_past_sla_rows()
        self._create_past_sla_dict(dataframe=sla_dataframe)
        self._add_common_destinations()
        self._sort_dictionary()
        self._get_sla_weight_sum()

    def _get_past_sla_rows(self):
        """
        Deletes any row in the DataFrame that contains "-" in the Days Column. This is to ensure that only past
        SLA rows are shown.
        :return: None
        """
        # Check if "-" in column 12. If "-" in column 12, return true. Returns all rows with "-"
        # ~ is used to invert the boolean value that is returned from this. Without the ~ it would only display
        # rows that don't contain "-". We only want to display values with "-".
        sla_report = self.table_data.drop(self.table_data[~self.table_data["Hours Remaining"].str.contains('-')].index)
        return sla_report

    def _create_past_sla_dict(self, dataframe: pd.DataFrame):
        """
        Store all the values in the "Route" column into a dictionary with the name of the "Route" being the key and then
        adding all the weight values that are associated with that route for the value key. Method uses the group
        method to group all the "Route" values and then sums up all the "Weight" values that are associated with that
        "Route" into a dictionary.

        :param dataframe: The DataFrame to modify.
        :return: None
        """
        self.convert_column_to_datatype(dataframe=dataframe, column_name="Weight", data_type="int")
        self.sla_data = dataframe.groupby('Route')['Weight'].sum().to_dict()

    def _add_common_destinations(self):
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

    def _sort_dictionary(self):
        """
        Sort SLA Data Dictionary by the destination with the highest number.
        :return: None
        """
        # Sort dictionary in reverse order (The Highest value first). Since sorted will return a
        # tuple, we use dict to convert it back to a dictionary. x[1] so we start at index 1 which is the values
        # the keys would be [0]
        self.sla_data = dict(sorted(self.sla_data.items(), key=lambda x: x[1], reverse=True))

    def bot_report_creation_data(self):
        """
        Calls all methods that are responsible for creating the Bot Report Data. Such methods are reformatting the Bot Report
        table (reformat_bot_report_table), only showing rows that are greater than the day_sorter value (sort_by_days),
        and sorting the columns to display the highest value in "Days" first (sort_column). Also changes the
        "Piece Count" and "Weight" columns to int, as they are originally set as strings.

        :return: None
        """
        self._reformat_bot_report_table()
        self._sort_by_days(dataframe=self.table_data)
        self.sort_column(dataframe=self.table_data, column_name="Days", ascending=False)
        self.table_data = self.convert_column_to_datatype(dataframe=self.table_data, column_name="Piece Count",
                                                          data_type='int')
        self.table_data = self.convert_column_to_datatype(dataframe=self.table_data, column_name="Weight",
                                                          data_type='int')
        self._get_highest_day(dataframe=self.table_data)

    def _get_highest_day(self, dataframe: pd.DataFrame):
        """
        Check if the "Days" column is empty. If it is, set highest_day to N/A (no values in row). Otherwise,
        set highest_day = to the highest value in the "Days" column.
        :param dataframe: The DataFrame to check.
        :return:
        """
        if len(dataframe["Days"]) == 0:
            self.highest_day = "N/A"
        else:
            self.highest_day = dataframe["Days"].max()

    def _reformat_bot_report_table(self):
        """
        Reformat the Bot Report Table by dropping "Hour Remaining" column, dropping any values that are empty in the
        "Recvd Date", dropping the first row as it contains nothing but a subheader. Also inserts necessary columns for
        the Bot Report table and adds values to the newly inserted "Days" column.
        :return: None
        """
        self.drop_columns(self.table_data, column_names=["Hours Remaining"])
        self.table_data.drop(self.table_data.index[0], inplace=True)
        self._drop_empty_values(self.table_data, column_name=["Recvd Date"])
        # Reset index, due to dropped columns.
        self.table_data = self.table_data.reset_index(drop=True)

        self.table_data = self.insert_column(self.table_data, last_column=True, column_name="Status")
        self.table_data = self.insert_column(self.table_data, last_column=True, column_name="Remarks")
        self.table_data = self.insert_column(self.table_data, last_column=False, column_name="Days", column_position=6)

        self._add_day_values(self.table_data)

    @classmethod
    def _drop_empty_values(cls, dataframe: pd.DataFrame, column_name: list):
        """
        Drop empty values that are in a column.
        :param dataframe: The DataFrame to modify.
        :param column_name: The list of columns to check of empty values.
        :return: None
        """
        dataframe.dropna(subset=column_name, inplace=True)

    def _add_day_values(self, dataframe: pd.DataFrame):
        """
        Get the current date and convert it to a Timestamp Object. The method will loop through the "Recvd Date"
        column and take the "Recvd Date" value and subtract it with today's date. This will give us how many days
        a piece of cargo has been in the system. It will then input that new value into the "Days" column. The value
        will be negative, so we use Abs to convert it to a positive integer. Lastly drop the "Recvd" Column, as it
        won't be used anymore.
        :param dataframe: The DataFrame to modify.
        :return: None
        """

        # Convert "Recvd Date" to Timestamp.
        self._modify_recd_column()

        today_date = pd.Timestamp(date.today())

        for i in range(len(dataframe["Recvd Date"])):
            delta = dataframe.at[i, "Recvd Date"] - today_date
            # Added +1 to include today's date.
            self.table_data.at[i, "Days"] = abs(delta.days) + 1

        self.drop_columns(dataframe, ["Recvd Date"])

    def _modify_recd_column(self):
        """
        This converts the "Recvd Date" Column to a Timestamp object.
        :return: None
        """
        self.table_data = self.convert_column_to_datatype(dataframe=self.table_data, column_name="Recvd Date",
                                                          data_type="datetime64[ns]")

    def _sort_by_days(self, dataframe: pd.DataFrame):
        """Remove any rows that are less than the value of day_sort. The day_sorter will contain the value
         from the SLA/Bot Report Setting (Days) entry box. This will sort the SLA/Bot Report to ensure only cargo
         that has been here passed a certain amount of days is shown.
         :return: None
         """

        self.table_data = dataframe[dataframe["Days"] >= self.day_sorter]

    def _get_sla_weight_sum(self):
        """
        Add up all the values in the sla_dict. This will get the total weight of all cargo that is past SLA.
        :return: None
        """
        self.sla_weight_sum = sum(self.sla_data.values())

    def get_awb_list(self):
        """
        Get a list of AWB's and store them in a dictionary. Where the key is the AWB number and value is another
        dictionary which contains the consignee, the community it's gonig to.
        :return: Returns a list of AWB's to use to search for AWB's in another class.
        """
        self.table_data = self.modify_column_string(dataframe=self.table_data, column_name="Consignment #",
                                                    replace_string="632-",
                                                    replace_string_with="")

        records = self.table_data.to_dict(orient="records")

        awb_dict = [{"AWB No.": record["Consignment #"], "Consignee": record["Consignee Name"].title(),
                     "Community": record["To"], "No. of Pieces": record["Pieces"]} for record in records]

        return awb_dict

    def _sort_home_delivery_awbs(self):
        # Use .copy() as you are not modifying the original data frame. You are filtering through the column
        # and creating a new dataframe for shipped_awb_data and not_shipped_awb_data
        self.shipped_awb_data = self.table_data[self.table_data["Flight Status"].str.contains("Allocated")].copy()
        self.not_shipped_awb_data = self.table_data[~self.table_data["Flight Status"].str.contains("Allocated")].copy()

    def _format_home_delivery_awbs(self):
        self._sort_home_delivery_awbs()

        self.drop_columns(dataframe=self.shipped_awb_data, column_names=["Flight Status"])
        self.drop_columns(dataframe=self.not_shipped_awb_data, column_names=["Consignee", "Flight Number",
                                                                             "Flight Date", "No. of Pieces"])
        self.shipped_awb_data["Flight Number"] = self.shipped_awb_data["Flight Number"].str.upper()
        self.sort_column(dataframe=self.shipped_awb_data, column_name="Flight Date", ascending=False)

        # Use apply method on the AWB No. Column. The apply method calls a function on the column (AWB No.)
        # We use lambda as the function call to store the current value in x and add 632- to it.
        self.shipped_awb_data["AWB No."] = self.shipped_awb_data["AWB No."].apply(lambda x: f"632-{x}")
        self.not_shipped_awb_data["AWB No."] = self.not_shipped_awb_data["AWB No."].apply(lambda x: f"632-{x}")

    def home_delivery_creation_data(self, awb_list: list):
        self.table_data = pd.DataFrame(awb_list)
        self._format_home_delivery_awbs()

        self.rename_columns(dataframe=self.shipped_awb_data, column_names={"Flight Number": "Flight No.",
                                                                     "Flight Date": "Date"})

        self.shipped_awb_data = self._rearrange_columns(dataframe=self.shipped_awb_data,
                                                  rearrange_column_names=["Date", "Flight No.", "Community",
                                                                          "AWB No.", "No. of Pieces", "Consignee"])