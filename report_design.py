import os
from openpyxl.styles import PatternFill, Border, Side, Alignment, Font
from openpyxl import load_workbook
import openpyxl
import pandas as pd
import tempfile
import shutil


class ReportDesign:
    def __init__(self, sla_data, bot_data):
        self.sla_data = sla_data
        self.bot_data = bot_data
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
                bot_dataframe.to_excel(writer, startrow=9 - 1, startcol=5 - 1, index=False)

    def header_design(self):
        sla_header = {"B8": "Destination", "C8": "Past SLA"}
        self.sheet["B8"].value = "Destination"
        self.sheet["C8"].value = "Past SLA"

        bot_headers = [key for key in self.bot_data]
        report_headers = self.get_cell_coordinates(bot_headers)
        report_headers.update(sla_header)

        for cell_cord in report_headers.keys():
            self.fill_color(cell_coordinate=cell_cord, hex_color='4285f4', fill_type='solid')
            self.change_font(cell_coordinate=cell_cord, bold=True)
            self.create_full_border(cell_coordinate=cell_cord)

        self.workbook.save(self.temp_file)

    def get_cell_coordinates(self, cell_text: list):
        coordinate_dict = {}
        for text in cell_text:
            for row in self.sheet.iter_rows():
                for cell in row:
                    if cell.value == text:
                        coordinate_dict[cell.coordinate] = cell.value

        return coordinate_dict

    def sla_table_design(self):

        # Start at row 9 and every second row, it will color those cells light blue.
        for row in range(9, len(self.sla_data) + 9):
            for col in ["B", "C"]:
                cell_cord = f"{col}{row}"
                if row % 2 == 0:
                    self.fill_color(hex_color="e8f0fe", fill_type='solid', cell_coordinate=cell_cord)

                self.create_full_border(cell_coordinate=cell_cord, border_type="thin")

        self.workbook.save(self.temp_file)

    def create_full_border(self, cell_coordinate: str, border_type: str = 'thin'):
        self.sheet[cell_coordinate].border = Border(left=Side(border_type), right=Side(border_type),
                                                    top=Side(border_type), bottom=Side(border_type))

    def change_font(self, cell_coordinate: str, font_name: str = "Calibri", size: int = 11, bold: bool = False,
                    font_color: str = "ffffff"):
        self.sheet[cell_coordinate].font = Font(name=font_name, size=size, bold=bold, color=font_color)

    def fill_color(self, hex_color: str, fill_type: str, cell_coordinate: str):
        self.sheet[cell_coordinate].fill = PatternFill(start_color=hex_color, end_color=hex_color, fill_type=fill_type)


    def open_temp_file(self):
        temp_name = self.temp_file
        self.workbook = load_workbook(temp_name)
        self.sheet = self.workbook.active

    def create_report(self):
        self.open_temp_file()
        self.header_design()
        self.sla_table_design()

    def create_excel_file(self):
        # Move Temp File for user to see
        shutil.move(self.temp_file, "output.xlsx")
