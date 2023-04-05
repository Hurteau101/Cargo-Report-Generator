import customtkinter as ctk
from pop_up_window import PopUpWindow


class ErrorWindow(PopUpWindow):
    """
    Class used to create an Error Pop-up Window.

      Attributes:
        - error_msg: Text to be put into the error window.

      Methods:
        - create_report: Creates SLA/Bot or Home Delivery Report
        - set_column_widths: Set column width
    """

    def __init__(self, theme: str, title: str, size: str, error_message):
        """
        Initializes a ErrorWindow Object.

        Creates the Textbox Widgets to display the Error Message.

        :param theme: Theme of the error window.
        :param title: Title of the error window.
        :param size: Size of the error window.
        :param error_message: Text to be put into the error window.
        """
        super().__init__(theme, title, size)

        self.error_msg = error_message
        self.error_textbox = ctk.CTkTextbox(master=self, text_color="red", wrap="word")
        self.error_textbox.pack(fill="both")
        self.insert_error_message()

    def insert_error_message(self) -> None:
        """
        Insert an error message into the textbox.
        """
        self.error_textbox.insert(ctk.END, self.error_msg)
        self.disable_textbox()

    def disable_textbox(self) -> None:
        """
        Disable the textbox.
        """
        self.error_textbox.configure(state=ctk.DISABLED)


