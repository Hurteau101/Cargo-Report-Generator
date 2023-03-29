from datetime import date, datetime
import os
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import openpyxl
import pandas as pd
import tempfile
import shutil
from utils import type_check


class ReportDesign:
    """
        A class for designing the Excel SLA/Bot Report and saving it as an Excel File.
        Class Utilizes the OpenPyxl Library.

       Main Attributes:
           - sla_data - All SLA data to be used in the Excel File.
           - bot_data - All Bot data to be used in the Excel File.
           - temp_file - A temporary file to be used to design the Excel file. A temporary file is used, to prevent
           the user from opening the report until all designs are completed.

       Main Operations:
           - insert_data_to_excel() - Inserts all SLA and Bot Data (Dictionary) into a temporary Excel file.
           - create_report() - Opens the temporary Excel File and creates all the designs necessary to create
           the Cargo Report.
           - _excel_settings() - Sets the Excel Settings, such as the name of the file, name of the sheet and if you
           want the Excel sheet to display gridlines.
       """
    def __init__(self, sla_data, bot_data, total_sla_weight, day_sorter, highest_day):
        self.sla_data = sla_data
        self.bot_data = bot_data
        self.day_sorter = day_sorter
        self.highest_day = highest_day
        self.total_sla_weight = total_sla_weight
        # Create Temp File Attribute.
        self.temp_file = None
        self.workbook = None
        self.sheet = None
        self.excel_name = None
        self.report_folder_path = None

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

    def _header_design(self):
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
        report_headers = self._get_cell_coordinates(bot_headers)
        report_headers.update(sla_header)

        for cell_cord in report_headers.keys():
            self._fill_color(cell_coordinate=cell_cord, hex_color='4285f4')
            self._change_font(cell_coordinate=cell_cord, bold=True)
            self._create_full_border(cell_coordinate=cell_cord)

    def _get_cell_coordinates(self, cell_text: list):
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

    def _sla_table_design(self):
        """
        This method is responsible for designing the SLA Table. Such things as setting every second row as light blue,
        setting borders around the table, changing the font and adding the total weight row to the SLA Table.
        :return: None
        """
        total_weight_row_number = self._add_total_weight_to_sla_table()

        # Start at row 9 and every second row, it will color those cells light blue.
        for row in range(9, len(self.sla_data) + 9):
            for col in ["B", "C"]:
                sla_data_cell_cord = f"{col}{row}"
                total_weight_cell_cord = f"{col}{total_weight_row_number}"
                if row % 2 == 0:
                    self._fill_color(hex_color="e8f0fe", cell_coordinate=sla_data_cell_cord)

                self._create_full_border(cell_coordinate=sla_data_cell_cord, border_type="thin")
                self._create_full_border(cell_coordinate=total_weight_cell_cord, border_type="thin")
                self._change_font(cell_coordinate=total_weight_cell_cord, bold=True)
                self._fill_color(cell_coordinate=total_weight_cell_cord, hex_color='4285f4')

        self._add_total_weight_to_sla_table()

    def _add_total_weight_to_sla_table(self):
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

    def _add_color_reference_cells(self):
        """
        This Method will add 4 cells on top of the Bot Report Table. The cells are just responsible for displaying
        color references. (Ex. F8 will contain "Going Today" with a fill color of green. Any cell in the Bot Report
        table which is colored green, means that cargo will be going today).
        :return: None
        """
        reference_data = {"E3": "Reference", "F3": "Going Today", "G3": "To Be Cleared", "H3": "On Hold"}
        for count, (cell_cord, cell_text) in enumerate(reference_data.items()):
            self.sheet[cell_cord].value = cell_text
            self._create_full_border(cell_coordinate=cell_cord)
            if count == 0:
                self._change_font(cell_coordinate=cell_cord, bold=True)
            else:
                self._change_font(cell_coordinate=cell_cord, bold=True, hex_color="000000")

        # reference_data contains the cell coordinates as the keys. Convert it to a list to access those keys.
        reference_data_keys = list(reference_data.keys())
        self._fill_color(cell_coordinate=reference_data_keys[0], hex_color="4285f4")
        self._fill_color(cell_coordinate=reference_data_keys[1], hex_color="00ff00")
        self._fill_color(cell_coordinate=reference_data_keys[2], hex_color="ffff00")
        self._fill_color(cell_coordinate=reference_data_keys[3], hex_color="ff0000")

    def _add_days_top_pri_table(self):
        """
        Create the top header for Days and Top Priority. Below the Days Text, it will get the value for day_sorter.
        The day sorter is the value in the SLA/Bot Report setting which is used to filter data by the number of days
        cargo has been in the warehouse. Below the Days TOP Pri, is the highest value in the "Days" column. All data
        is obtained from the table_data class. Method also formats this small table to the approriate colors, borders
        and font.
        :return: None
        """
        day_pri_values = {"E5": "DAYS", "E6": self.day_sorter, "H5": "Days TOP PRI", "H6": self.highest_day}

        for cell_cord, cell_text in day_pri_values.items():
            self.sheet[cell_cord].value = cell_text
            self._change_font(cell_coordinate=cell_cord, bold=True)
            self._fill_color(cell_coordinate=cell_cord, hex_color="7A7A7A")

        self._fill_color(cell_coordinate="F5", hex_color="7A7A7A")
        self.sheet.merge_cells("F5:G6")

    def _add_date(self):
        """
        Add the current date to the Cargo Report.
        :return: None
        """
        today = date.today()
        formatted_date = today.strftime("%B %d, %Y")
        self.sheet["L5"].value = formatted_date
        self._change_font(cell_coordinate="L5", size=18, hex_color="000000")
        self.sheet["L5"].alignment = Alignment(vertical="center")
        self.sheet.merge_cells("L5:M6")

    def _add_logo(self):
        """
        Add the logo to the Cargo Report.
        :return: None
        """
        img = Image("logo.png")
        self.sheet.add_image(img, 'B2')

    def get_date_time(self):
        """
        Get the current date and time. This method is used if you want to save the Cargo Report by the date and time.
        (Ex. Cargo Report on February 28, 2023 - 1236AM".
        :return:
        """
        today_date = datetime.today()
        current_date_time = today_date.strftime("%B %d, %Y - %#I%M%p")
        return current_date_time

    def _create_sla_bot_report_folder(self, folder_name):
        """
        Creates a folder in the current working directory based on the folder_name argument. It will check if the
        folder doesn't exist. If it doesn't, it will create a folder.
        :param folder_name:
        :return:
        """
        current_director = os.getcwd()
        self.report_folder_path = os.path.join(current_director, folder_name)
        if not os.path.isdir(folder_name):
            os.mkdir(self.report_folder_path)

    def _excel_settings(self, save_name_as: str, sheet_title: str, show_gridlines: bool = False):
        """
        Set the Excel settings, such as the name of the file, the name of the sheet and if you want the Report
        to show gridlines.
        :param save_name_as: Name of the Excel File.
        :param sheet_title: Name of the Excel Sheet.
        :param show_gridlines: If you want to show the gridlines on Excel. True = Yes | False = No
        (Default value: False)
        :return: None
        """
        self.excel_name = save_name_as
        self.sheet.title = sheet_title

        if show_gridlines:
            self.sheet.sheet_view.showGridLines = True
        else:
            self.sheet.sheet_view.showGridLines = False

    def _all_cells_style(self, horizontal_alignment: str = "center"):
        """
        Method is responsible for changing the style of ALL cells in the Excel document.
        :param horizontal_alignment: Set the horizontal alignment for all cells. (Default: "center")
        :return: None
        """
        for row in self.sheet.iter_rows():
            for cell in row:
                cell.alignment = Alignment(horizontal=horizontal_alignment)

    def _set_columns_widths(self, column_custom_width: dict):
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
    def _get_custom_column_widths(cls):
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
            "G": 17,
            "H": 17,
            "I": 17,
            "J": 17,
            "K": 17,
            "L": 17,
            "M": 17,
        }

        return custom_column_width

    def _get_columns_with_text(self):
        """
        Get a list of columns that contain text (Ex. A, B, C)
        :return: Returns all columns that contain text.
        """

        column_with_text = [get_column_letter(cell.column) for col in self.sheet.iter_cols()
                            for cell in col if cell.value is not None]

        return column_with_text

    def _create_full_border(self, cell_coordinate: str, border_type: str = 'thin'):
        """
        Creates a border around a specific cell.
        :param cell_coordinate: Coordinate of the cell you want the border around. (Ex. E10)
        :param border_type: Set the type of border you want. (Default: 'thin')
        :return: None
        """
        self.sheet[cell_coordinate].border = Border(left=Side(border_type), right=Side(border_type),
                                                    top=Side(border_type), bottom=Side(border_type))

    def _change_font(self, cell_coordinate: str, font_name: str = "Calibri", size: int = 11, bold: bool = False,
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

    def _fill_color(self, cell_coordinate: str, hex_color: str, fill_type: str = "solid"):
        """
        Change the fill color of a specific cell.
        :param cell_coordinate: Coordinate of the cell you want to fill. (Ex. E10)
        :param hex_color: Color you want to fill with. Make sure its in hex value without '#'. (Ex. 'ffffff')
        :param fill_type: Set a pattern or color gradient (Default: 'solid")
        :return: None
        """
        self.sheet[cell_coordinate].fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type=fill_type)

    def _open_temp_file(self):
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
        self._open_temp_file()
        self._header_design()
        self._sla_table_design()
        self._set_columns_widths(column_custom_width=self._get_custom_column_widths())
        self._add_color_reference_cells()
        self._add_days_top_pri_table()
        self._add_date()
        self._add_logo()
        self._all_cells_style(horizontal_alignment="center")
        self._excel_settings(save_name_as=f"Cargo Report on {self.get_date_time()}.xlsx",
                             sheet_title="Cargo Report", show_gridlines=False)
        self._save_temp_file()

    def _save_temp_file(self):
        self.workbook.save(self.temp_file)

    def create_excel_file(self):
        """
        Method is responsible for first creating a "Cargo Report" folder if it doesn't exist. It will then move
        the temporary file into the "Cargo Report" folder for the user to view/use. Use this method
        last, as the user will be able to see the file once this method is called.
        :return: None
        """
        self._create_sla_bot_report_folder("Cargo Report")

        # Move Temp File for user to see
        shutil.move(self.temp_file, f"{self.report_folder_path}/{self.excel_name}")
