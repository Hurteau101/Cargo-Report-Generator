import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()
SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
UID = os.getenv("UID")
PWD = os.getenv("PWD")


class DatabaseConnector:
    def __init__(self):
        self.connection = None

    @property
    def connection_string(self):
        return f'Driver={{SQL Server}};Server={SERVER_NAME};Database={DATABASE_NAME};UID={UID};PWD={PWD};Trusted_Connection=no'

    def connect(self):
        self.connection = pyodbc.connect(self.connection_string)

    def close_conn(self):
        if self.connection:
            self.connection.close()


