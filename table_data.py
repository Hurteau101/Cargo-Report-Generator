import pandas as pd

class TableData:
    def __init__(self, waybill_table):
        self.waybill_data_table = pd.read_html(waybill_table)[0]

    def test(self):
        print(self.waybill_data_table)