import os
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import openpyxl
import pandas as pd
import tempfile
import shutil
from utils import type_check


class ReportDesign:
    def __init__(self, sla_data, bot_data, total_sla_weight):
        self.sla_data = sla_data
        self.bot_data = bot_data
        self.total_sla_weight = total_sla_weight
        # Create Temp File Attribute.
        self.temp_file = None
        self.workbook = None
        self.sheet = None

    def insert_data_to_excel(self):
        """
        Insert dictionary data into Excel file.
        This method will insert the SLA and Bot dictionary into an Excel File. It saves it as a temp file,
        as there will be other methods to re-design the Excel file. Saving it as temp, will prevent the user from
        accidentally opening it.
        :return: None
        """
        with tempfile.NamedTemporaryFile(suffix=".xlsx", delete=False) as temp:
            self.temp_file = temp.name

            # Create a bot_dataframe from self.bot_data
            sla_dataframe = pd.DataFrame(self.sla_data, index=[0]).T
            bot_dataframe = pd.DataFrame(self.bot_data)

            with pd.ExcelWriter(temp.name) as writer:
                # Write the bot_dataframe to the Excel file
                sla_dataframe.to_excel(writer, startrow=9 - 1, startcol=2 - 1, header=False)
                bot_dataframe.to_excel(writer, startrow=8 - 1, startcol=5 - 1, index=False)

    def header_design(self):
        """
        This method is responsible for designing ALL header designs in the Excel Report. There are 2 different
        reports in the SLA/Bot Report (SLA Report and Bot Report). It will create the SLA Headers and then loop
        through all the headers for SLA and Bot Report and change the fill color, font and create borders.
        :return: None
        """
        sla_header = {"B8": "Destination", "C8": "Past SLA"}
        self.sheet["B8"].value = "Destination"
        self.sheet["C8"].value = "Past SLA"

        bot_headers = [key for key in self.bot_data]
        report_headers = self.get_cell_coordinates(bot_headers)
        report_headers.update(sla_header)

        for cell_cord in report_headers.keys():
            self.fill_color(cell_coordinate=cell_cord, hex_color='4285f4')
            self.change_font(cell_coordinate=cell_cord, bold=True)
            self.create_full_border(cell_coordinate=cell_cord)

    def get_cell_coordinates(self, cell_text: list):
        """
        This will get the cell coordinates based on text. It will loop through the Excel document and find the text
        that matches the passed in cell_text dictionary. It will then create a dictionary where the key is the
        cell coordinate (ex. E10) and the values will be the value inside that cell coordinate (ex. Route).
        :param cell_text: List of words to find where they are located in the Excel Document.
        :return: Returns the coordinates and values of the found text.
        """
        coordinate_dict = {}
        for text in cell_text:
            for row in self.sheet.iter_rows():
                for cell in row:
                    if cell.value == text:
                        coordinate_dict[cell.coordinate] = cell.value

        return coordinate_dict

    def sla_table_design(self):
        """
        This method is responsible for designing the SLA Table. Such things as setting every second row as light blue,
        setting borders around the table, changing the font and adding the total weight row to the SLA Table.
        :return: None
        """
        total_weight_row_number = self.add_total_weight_to_sla_table()

        # Start at row 9 and every second row, it will color those cells light blue.
        for row in range(9, len(self.sla_data) + 9):
            for col in ["B", "C"]:
                sla_data_cell_cord = f"{col}{row}"
                total_weight_cell_cord = f"{col}{total_weight_row_number}"
                if row % 2 == 0:
                    self.fill_color(hex_color="e8f0fe", cell_coordinate=sla_data_cell_cord)

                self.create_full_border(cell_coordinate=sla_data_cell_cord, border_type="thin")
                self.create_full_border(cell_coordinate=total_weight_cell_cord, border_type="thin")
                self.change_font(cell_coordinate=total_weight_cell_cord, bold=True)
                self.fill_color(cell_coordinate=total_weight_cell_cord, hex_color='4285f4')

        self.add_total_weight_to_sla_table()

    def add_total_weight_to_sla_table(self):
        """
        This method will get the length of the sla_data dictionary. This will tell us how many rows there will be. It
        then adds 10 to that, to allow an empty row between the sla_data and the total weight row. The value 10 is set
        because the sla_data starts at row 9, and we want to add 1 empty row between that (9 + 1 = 10).
        :return: Returns row number of the total weight row.
        """

        # Get the length of sla_data to tell us how many rows there are. Add 10 to that, to allow an empty row between
        # the data and the total weight. 10 is there since we start at row 9, then add 1 empty row so 9 + 1 = 10.
        total_sla_rows = len(self.sla_data) + 10
        self.sheet[f"B{total_sla_rows}"].value = "Total"
        self.sheet[f"C{total_sla_rows}"].value = self.total_sla_weight

        return total_sla_rows

    def all_cells_style(self, horizontal_alignment: str = "center"):
        """
        Method is responsible for changing the style of ALL cells in the Excel document.
        :param horizontal_alignment: Set the horizontal alignment for all cells. (Default: "center")
        :return: None
        """
        for row in self.sheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal=horizontal_alignment)

    def set_columns_widths(self, column_custom_width: dict):
        """
        Responsible for setting the column widths of the specified columns.

        :param column_custom_width:  Pass in a dictionary where the Keys are the columns (Ex. A, B) and the values are
        the width you want to set that column to (Ex. 50). (Ex. column_custom_width = {"A": 100, "B": 50}
        :return: None
        """
        # Ensure that the column_custom_width dictionary is in the proper format. The keys are actual column names
        # (Ex. 'A' or 'B' or 'C') and the values (width) are int datatype.
        for column_name, width in column_custom_width.items():
            type_check(arg=width, arg_name="width", expected_type=int)
            if not column_name.isalpha() or len(column_name) != 1:
                raise ValueError(f"Please ensure when passing column_custom_width that the Keys are"
                                 f" the name of the column. (Ex. 'A' or 'B' or 'C'")
            else:
                self.sheet.column_dimensions[column_name].width = width



    @classmethod
    def get_custom_column_widths(cls):
        """
        Set the specified columns in the Excel Document by a specific width. This will be used in the all_cells_style
        method when you pass in a column_custom_width argument.
        :return: Returns a dictionary of column names as the keys and the width as the values.
        """
        custom_column_width = {
            "B": 15,
            "C": 15,
            "E": 13,
            "F": 17,
            "G": 25,
            "H": 50,
            "I": 13,
            "J": 13,
            "K": 13,
            "L": 17,
            "M": 40,
        }

        return custom_column_width

    def get_columns_with_text(self):
        """
        Get a list of columns that contain text (Ex. A, B, C)
        :return: Returns all columns that contain text.
        """

        column_with_text = [get_column_letter(cell.column) for col in self.sheet.iter_cols()
                            for cell in col if cell.value is not None]

        return column_with_text

    def create_full_border(self, cell_coordinate: str, border_type: str = 'thin'):
        """
        Creates a border around a specific cell.
        :param cell_coordinate: Coordinate of the cell you want the border around. (Ex. E10)
        :param border_type: Set the type of border you want. (Default: 'thin')
        :return: None
        """
        self.sheet[cell_coordinate].border = Border(left=Side(border_type), right=Side(border_type),
                                                    top=Side(border_type), bottom=Side(border_type))

    def change_font(self, cell_coordinate: str, font_name: str = "Calibri", size: int = 11, bold: bool = False,
                    hex_color: str = "ffffff"):
        """
        Change the font of a specific cell.
        :param cell_coordinate: Coordinate of the cell you want to change the font for. (Ex. E10)
        :param font_name: Name of the font (Default: 'Calibri')
        :param size: Size of the font (Default: 11)
        :param bold: Set bold font. True = Bold | False = Not Bold (Default: false)
        :param hex_color: Color you want the font to be. Make sure its in hex value without '#'.
        (Default = 'ffffff' [White Color])
        :return: None
        """
        self.sheet[cell_coordinate].font = Font(name=font_name, size=size, bold=bold, color=hex_color)

    def fill_color(self, cell_coordinate: str, hex_color: str, fill_type: str = "solid"):
        """
        Change the fill color of a specific cell.
        :param cell_coordinate: Coordinate of the cell you want to fill. (Ex. E10)
        :param hex_color: Color you want to fill with. Make sure its in hex value without '#'. (Ex. 'ffffff')
        :param fill_type: Set a pattern or color gradient (Default: 'solid")
        :return: None
        """
        self.sheet[cell_coordinate].fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type=fill_type)

    def open_temp_file(self):
        """
        Opens the temporary Excel file. The temporary Excel file is first created in the insert_data_to_excel method.
        We then can open it to style the Excel File. Using a temporary file to avoid the user from opening the file
        in the directory until all styling is done. We are also setting a workbook and sheet with OpenPyxl to allow
        other methods to modify the Excel file.
        :return: None
        """
        temp_name = self.temp_file
        self.workbook = load_workbook(temp_name)
        self.sheet = self.workbook.active

    def create_report(self):
        """
        Method is responsible for opening the temp file and creating all designs of the Excel document.
        :return:
        """
        self.open_temp_file()
        self.all_cells_style(horizontal_alignment="center")
        self.header_design()
        self.sla_table_design()
        self.set_columns_widths(column_custom_width=self.get_custom_column_widths())
        self.save_temp_file()

    def save_temp_file(self):
        self.workbook.save(self.temp_file)

    def create_excel_file(self):
        """
        Method is responsible for moving the temporary file into the directory for the user to view/use. Use this method
        last, as the user will be able to see the file once this method is called.
        :return: None
        """
        # Move Temp File for user to see
        shutil.move(self.temp_file, "output.xlsx")
