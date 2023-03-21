import customtkinter as ctk
from datetime import datetime
from dateutil.relativedelta import relativedelta


class SettingWindow(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.geometry("500x490")
        self.bind("<FocusIn>", self.on_focus_in)  # Focus in on window once its open.
        self.grab_set()  # Prevent main window from being usable until this window is closed.
        self.title("Settings")
        self.maxsize(500, 490)
        self.minsize(500, 490)

        # Create Frames
        self.create_main_frame()
        self.create_bot_sla_frame()
        self.create_home_delivery_frame()

        # Create Widgets
        self.create_bot_sla_widgets(self.bot_sla_frame)
        self.create_home_delivery_widgets(self.home_frame)

        # Set Default Values
        self.default_day_value()
        self.default_from_month_value()
        self.default_from_day_value()
        self.default_to_date_value()
        self.default_to_airport_value()
        self.default_from_airport_value()
        self.default_top_pri_value()
        self.default_keyword_value()

    def create_main_frame(self):
        """Main Setting Frame"""
        self.main_frame = ctk.CTkFrame(master=self, fg_color="transparent")
        self.main_frame.pack()

    def create_bot_sla_frame(self):
        """Bot/SLA Frame"""
        self.bot_sla_frame = ctk.CTkFrame(master=self.main_frame, height=430)
        self.bot_sla_frame.pack_propagate(False)
        self.bot_sla_frame.pack(side="left", padx=(0, 30), pady=(30, 0))

    def create_home_delivery_frame(self):
        """Home Delivery Frame"""
        self.home_frame = ctk.CTkFrame(master=self.main_frame, height=430)
        self.home_frame.pack_propagate(False)
        self.home_frame.pack(side="left", pady=(30, 0))

    def create_bot_sla_widgets(self, frame):
        self.bot_heading_label = ctk.CTkLabel(master=frame, text="Bot/SLA Report Settings", font=("Helvetica", 12,
                                                                                                  "bold", "underline"))
        self.bot_heading_label.pack()

        self.days_label = ctk.CTkLabel(master=frame, text="Days")
        self.days_label.pack()

        self.days_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="8", justify="center")
        self.days_box.pack()

        self.top_priority_label = ctk.CTkLabel(master=frame, text="Top Priority")
        self.top_priority_label.pack()

        # TODO: Add placeholder
        self.top_priority_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="-6", justify="center")
        self.top_priority_box.pack()

        self.from_month_back_sla_label = ctk.CTkLabel(master=frame, text="Number of Months Back")
        self.from_month_back_sla_label.pack()

        self.from_month_back_sla_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="2",
                                                    justify="center")
        self.from_month_back_sla_box.pack()

        self.from_day_back_sla_label = ctk.CTkLabel(master=frame, text="Number of Days Back", justify="center")
        self.from_day_back_sla_label.pack()

        self.from_day_back_sla_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="0",
                                                  justify="center")
        self.from_day_back_sla_box.pack()

        self.to_date_sla_label = ctk.CTkLabel(master=frame, text="To Date")
        self.to_date_sla_label.pack()

        self.to_date_sla_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="20-Jan-2023", justify="center")
        self.to_date_sla_box.pack()

        self.from_airport_sla_label = ctk.CTkLabel(master=frame, text="From Airport")
        self.from_airport_sla_label.pack()

        self.from_airport_sla_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="WPG", justify="center")
        self.from_airport_sla_box.pack()

        self.to_airport_sla_label = ctk.CTkLabel(master=frame, text="To Airport")
        self.to_airport_sla_label.pack()

        self.to_airport_sla_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="Please Select",
                                               justify="center")
        self.to_airport_sla_box.pack()

    def create_home_delivery_widgets(self, frame):


        self.home_heading_label = ctk.CTkLabel(master=frame, text="Home Delivery Settings", font=("Helvetica", 12,
                                                                                                  "bold", "underline"))
        self.home_heading_label.pack()

        label_list = ["Number of Months Back", "Number of Days Back"]
        for label_text in label_list:
            label = ctk.CTkLabel(master=frame, text=label_text)
            label.pack()

        # self.from_month_back_home_label = ctk.CTkLabel(master=frame, text="Number of Months Back")
        # self.from_month_back_home_label.pack()
        #
        # self.from_month_back_home_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="2",
        #                                              justify="center")
        # self.from_month_back_home_box.pack()
        #
        # self.from_day_back_home_label = ctk.CTkLabel(master=frame, text="Number of Days Back", justify="center")
        # self.from_day_back_home_label.pack()
        #
        # self.from_day_back_home_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="0",
        #                                           justify="center")
        # self.from_day_back_home_box.pack()
        #
        # self.to_date_home_label = ctk.CTkLabel(master=frame, text="To Date")
        # self.to_date_home_label.pack()
        #
        # self.to_date_home_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="20-Jan-2023", justify="center")
        # self.to_date_home_box.pack()
        #
        # self.from_airport_home_label = ctk.CTkLabel(master=frame, text="From Airport")
        # self.from_airport_home_label.pack()
        #
        # self.from_airport_home_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="WPG", justify="center")
        # self.from_airport_home_box.pack()
        #
        # self.to_airport_home_label = ctk.CTkLabel(master=frame, text="To Airport")
        # self.to_airport_home_label.pack()
        #
        # self.to_airport_home_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="Please Select",
        #                                         justify="center")
        # self.to_airport_home_box.pack()
        #
        # self.keyword_label = ctk.CTkLabel(master=frame, text="Keyword")
        # self.keyword_label.pack()
        #
        # self.keyword_box = ctk.CTkEntry(master=frame, width=100, placeholder_text="SYSCO", justify="center")
        # self.keyword_box.pack()

    def default_day_value(self):
        """Set default day value. This is used for sorting the Bot/SLA Report Excel File"""
        self.days_box.insert(ctk.END, "8")

    def default_from_day_value(self):
        """Set the default amount of months to go back"""
        self.from_day_back_sla_box.insert(ctk.END, "0")
        self.from_day_back_home_box.insert(ctk.END, "2")

    def default_from_month_value(self):
        self.from_month_back_sla_box.insert(ctk.END, "2")
        self.from_month_back_home_box.insert(ctk.END, "0")

    def default_to_date_value(self):
        """The default to date"""
        default_date = datetime.today().date()
        self.to_date_home_box.insert(ctk.END, default_date.strftime("%d-%b-%Y"))
        self.to_date_sla_box.insert(ctk.END, default_date.strftime("%d-%b-%Y"))

    def default_to_airport_value(self):
        """Set default to airport"""
        self.to_airport_home_box.insert(ctk.END, "Please Select")
        self.to_airport_sla_box.insert(ctk.END, "Please Select")

    def default_from_airport_value(self):
        """Set the default from airport"""
        self.from_airport_sla_box.insert(ctk.END, "WPG")
        self.from_airport_home_box.insert(ctk.END, "WPG")

    def default_top_pri_value(self):
        """Set the default top priority value for the Bot/SLA Report Excel File"""
        self.top_priority_box.insert(ctk.END, "-6")

    def default_keyword_value(self):
        """Set the default keyword for when searching with Home Delivery Report"""
        self.keyword_box.insert(ctk.END, "SYSCO")

    def on_focus_in(self, event):
        """Bring setting window to the front when opened"""
        self.attributes("-topmost", True)
