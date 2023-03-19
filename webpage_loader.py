from webpage_settings import WebpageSettings
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
        if self._password is None or self._username is None:
            self.quit_selenium()
            raise ValueError("Username and Password must be set before attempting to login.")

    def check_webpage_loaded(self, element: str, wait_time: int, error_message: str = None):
        """Check if a webpage is loaded or not.
        Pass in the XPATH string, the wait time length and an optional error message"""
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located((By.XPATH, element)))
        except TimeoutException:
            # TODO: Add popup to let user know page didn't load correctly
            if error_message is None:
                print("Webpage Timeout")
            else:
                print(error_message)
            return False

        return True

    def check_login(self):
        if not self.check_webpage_loaded("//div[@class='DlinkLoggedIn']//a[normalize-space()='Logout']",
                                         wait_time=5, error_message="Login Failed"):
            return False
        return True

    def login(self):
        self._validate_credentials()
        if self.check_webpage_loaded("//input[@id='UserName']", 5):
            username_field = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
            username_field.send_keys(self.username)

            password_field = self.driver.find_element(By.XPATH, "//input[@id='pwd']")
            password_field.send_keys(self.password)

            login_button = self.driver.find_element(By.XPATH, "//button[@id='load2']")
            login_button.click()

            return self.check_login()

        return False

