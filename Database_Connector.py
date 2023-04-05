import pyodbc
import os
from dotenv import load_dotenv

# Environment Variables to load sensitive information.
load_dotenv()
SERVER_NAME = os.getenv("SERVER_NAME")
DATABASE_NAME = os.getenv("DATABASE_NAME")
UID = os.getenv("UID")
PWD = os.getenv("PWD")


class DatabaseConnector:
    """
    A class for setting up a connection to a SQL Server database.

     Attributes:
        - connection (pyodbc.connect): Connection for a Database
     Methods:
        - connection_string(): Returns the connection string for SQL Server.
        - connect(): Connects to the SQL Server database.
        - close_conn(): Closes the connection to the SQL Server database if it's open.
    """

    def __init__(self):
        """Initialize a new DatabaseConnector instance."""
        self.connection = None

    @property
    def connection_string(self) -> str:
        """Return the connection string for SQL Server.

        Returns:
            str: The connection string for SQL Server.
        """
        return f'Driver={{SQL Server}};Server={SERVER_NAME};Database={DATABASE_NAME};UID={UID};PWD={PWD};Trusted_Connection=no'

    def connect(self) -> None:
        """Connect to SQL Server.

        Raises:
            pyodbc.Error: If the connection fails.
        """
        self.connection = pyodbc.connect(self.connection_string)

    def close_conn(self) -> None:
        """Close Connection to SQL Server if its open"""
        if self.connection:
            self.connection.close()


