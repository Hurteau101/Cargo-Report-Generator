import customtkinter as ctk
from datetime import datetime


class CargoInterface(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cargo Interface")
        self.geometry("500x350")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        self.resizable(False, False)

        # Main Frame Layout
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(expand=True, fill="both")

        # Tab Layout
        self.tabview = ctk.CTkTabview(self.main_frame)
        self.tabview.pack(expand=True, fill="both")
        self.tabview.add("SLA/Bot Report")
        self.tabview.add("Home Delivery")

        # SLA/Bot Report - Setting Frame
        self.setting_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"), height=40)
        self.setting_frame.pack(fill="x", pady=(10, 20))

        # SLA/Bot Report - Main Frame
        self.main_frame = ctk.CTkFrame(self.tabview.tab("SLA/Bot Report"))
        self.main_frame.pack(fill="x", pady=(0, 10))

        # Settings Layout
        self.setting_label = ctk.CTkLabel(master=self.setting_frame, text="Settings:")
        self.setting_label.grid(row=0, column=0, sticky="w", pady=5, padx=(10, 10))

        self.day_label = ctk.CTkLabel(master=self.setting_frame, text="Days")
        self.day_label.grid(row=1, column=0, sticky="w", pady=10, padx=(10, 0))
        self.days_combobox = ctk.CTkComboBox(self.setting_frame,
                                             values=["1", "2", "3", "4", "5", "6", "7", "8"])
        self.days_combobox.grid(row=1, column=1, sticky="w", padx=(0, 50))

        self.from_date_label = ctk.CTkLabel(master=self.setting_frame, text="Date From:")
        self.from_date_label.grid(row=1, column=2)

        self.from_date_entry = ctk.CTkEntry(master=self.setting_frame,
                                            placeholder_text=self.place_holder_date(),
                                            placeholder_text_color="gray")
        self.from_date_entry.grid(row=1, column=3, padx=(10, 0))

        # SLA/Bot Report - Main Layout
        self.button = ctk.CTkButton(master=self.main_frame, text="Webpage Load")
        self.button.grid(row=0, column=0)

    @classmethod
    def place_holder_date(cls):
        today_date = datetime.today().date()
        return today_date.strftime("%d-%b-%Y")


cargo = CargoInterface()
cargo.mainloop()
