from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date
import time


class CargoWebpage:
    def __init__(self):
        self._username = None
        self._password = None
        self.driver = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password):
        self._password = password

    def load_url(self, url):
        self.driver.get(url)

    def start_selenium(self, options=None):
        """Use method to start Selenium Webdriver. Use WebpageSettings.headless_chrome as argument to set Selenium to
        headless mode"""
        service = Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def quit_selenium(self):
        self.driver.quit()

    def _validate_credentials(self):
        """Check if username and password were passed in"""
        if self._password is None or self._username is None:
            self.quit_selenium()
            raise ValueError("Username and Password must be set before attempting to login.")

    def check_webpage_loaded(self, element: str, wait_time: int):
        """Check if a webpage is loaded or not.
        Pass in the XPATH string, the wait time length and an optional error message"""
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, element)))
        except TimeoutException:
            self.quit_selenium()
            return False

        return True

    def check_login(self):
        """Check if user profile is visible. If it is, login was successful. If not, then login failed. """
        return self.check_webpage_loaded(element="//div[@class='DlinkLoggedIn']//a[normalize-space()='Logout']",
                                         wait_time=2)

    def login(self):
        self._validate_credentials()
        username_field = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.XPATH, "//input[@id='pwd']")
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, "//button[@id='load2']")
        login_button.click()

    def waybills_to_ship_page(self):
        self.load_url("https://cargo.perimeter.ca/webmaster/reports/GeneralReport/Default?report_id=75")
        if self.check_webpage_loaded("//input[@id='txt_from_date75']", wait_time=5):
            return True
        return False

    @classmethod
    def today_date(cls):
        today = date.today()
        return today.strftime("%d-%b-%Y")

    def waybills_data(self, from_date: str):
        from_date_field = self.driver.find_element(By.XPATH, "//input[@id='txt_from_date75']")
        from_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                                "4]/div/div[2]/div/select")
        to_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                              "5]/div/div[2]/div/select")



