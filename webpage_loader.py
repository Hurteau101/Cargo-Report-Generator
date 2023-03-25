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
    """
    Class to handle interactions with a Cargo webpage using Selenium WebDriver.

    Main Attributes:
        _username (str): The username for the Cargo webpage.
        _password (str): The password for the Cargo webpage.
        driver (WebDriver): The Selenium WebDriver instance used to interact with the webpage.

    Main Operations:
        - load_url(url: str): Load the given URL in the web driver.
        - start_selenium(options: Optional[ChromeOptions]): Start the Selenium WebDriver. Optionally provide ChromeOptions to run in headless mode.
        - quit_selenium(): Quit the Selenium WebDriver.
        - check_webpage_loaded(element: str, wait_time: int): Check if the given webpage element is loaded within the given wait time.
        - check_login(): Check if the user is logged into the Cargo webpage.
    """
    def __init__(self):
        self._username = None
        self._password = None
        self.driver = None

    @property
    def username(self) -> str:
        """
        Get the username
        :return: Returns the username.
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """
        Set username
        :param username: The username for the cargo webpage.
        :return: None
        """
        self._username = username

    @property
    def password(self) -> str:
        """
        Get the password
        :return: Returns the password
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """
        Set password
        :param password:  The password for the cargo webpage.
        :return: None
        """
        self._password = password

    def load_url(self, url: str):
        """
        Loads the specified url.
        :param url: The URL of the webpage you want to load.
        :return: None
        """
        self.driver.get(url)

    def start_selenium(self, options: webdriver.ChromeOptions = None):
        """
        Starts Selenium Webdriver.

        :param options: The options will put Selenium into headless mode.
        Valid option is WebpageSettings.headless_chrome. (ex. options = WebpageSettings.headless_chrome())
        """
        service = Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)

    def quit_selenium(self):
        """
        Quits Selenium Webdriver.
        :return: None.
        """
        self.driver.quit()

    def _validate_credentials(self):
        """
        Checks to see if the username and password have been set for this instance of the CargoWebpage class.

        If either the username or password have not been set, this method raises a ValueError exception and
        quits the Selenium driver.

        :return: None
        """
        if self._password is None or self._username is None:
            self.quit_selenium()
            raise ValueError("Username and Password must be set before attempting to login.")

    def check_webpage_loaded(self, element: str, wait_time: int) -> bool:
        """Check if a webpage is loaded or not.

        This method checks to see if a webpage is loaded correctly. It does this by checking if it can find the
        specified element that is passed as an argument is on the page. The element argument must be passed as an XPATH
        string. The wait_time argument tells selenium how long to wait. If it can't find that element within that
        time frame, it will quit selenium and return False. The method also ensures the element argument is a string
        and the wait_time argument is an int, if it's not it will raise an execption.

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

    def check_login(self) -> bool:
        """
        Checks to see if the user has successfully signed in to the webpage on the script.

        The method checks to see if the script was able to sucessfully log in. It does this by checking to see if
        it can locate the "logout" button on the webpage. It does that by locating the "logout" xpath. The method
        calls "check_webpage_loaded" to see if the "logout" button was found on the webpage, which means the webpage
        was loaded correctly.

        :return: Returns True if it can find the "logout" element on the webpage (successful login), otherwise false.
        """

        return self.check_webpage_loaded(element="//div[@class='DlinkLoggedIn']//a[normalize-space()='Logout']",
                                         wait_time=2)

    def login(self):
        """
        Allows the script to log in to the Cargo Webpage.

        The method allows the script to get the XPATH for the username and password fields. It then inputs the username
        and password attributes and sends the keys to the webpage, which allows it to login.

        :return: None
        """
        """Login into the webpage"""
        self._validate_credentials()
        username_field = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
        username_field.send_keys(self.username)

        password_field = self.driver.find_element(By.XPATH, "//input[@id='pwd']")
        password_field.send_keys(self.password)

        login_button = self.driver.find_element(By.XPATH, "//button[@id='load2']")
        self.today_date()
        login_button.click()

    # TODO: Add docstring when method is finished.
    def waybills_to_ship_page(self, url: str) -> bool:
        self.load_url(url)
        if self.check_webpage_loaded("//input[@id='txt_from_date75']", wait_time=5):
            return True
        return False

    @classmethod
    def today_date(cls):
        """
        Get today's date.
        The method gets today's date and formats the date into a string. The reformatted date looks like: 24-Mar-2023
        :return: Returns the current day but reformatted into a string. (Ex. 24-Mar-2023)
        """
        today = date.today()
        return today.strftime("%d-%b-%Y")

    # TODO: Add docstring when method is finished.
    def waybills_data(self, from_date: str):
        from_date_field = self.driver.find_element(By.XPATH, "//input[@id='txt_from_date75']")
        from_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                                "4]/div/div[2]/div/select")
        to_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                              "5]/div/div[2]/div/select")



