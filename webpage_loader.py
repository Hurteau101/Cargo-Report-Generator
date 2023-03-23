from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date
import time
from utils import type_check


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
        """Use method to start Selenium Webdriver.

        :param options: The options will put Selenium into headless mode.
        Valid option is WebpageSettings.headless_chrome
        """
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

        :param element: The XPATH of the element.
        :param wait_time: The length of time you want to wait for the element to appear. Make sure it's an integer
        """
        type_check(arg=element, arg_name="element", expected_type=str)
        type_check(arg=wait_time, arg_name="wait_time", expected_type=int)

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
        """Login into the webpage"""
        self._validate_credentials()
        username_field = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.XPATH, "//input[@id='pwd']")
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, "//button[@id='load2']")
        login_button.click()

    def waybills_to_ship_page(self, url):
        self.load_url(url)
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



