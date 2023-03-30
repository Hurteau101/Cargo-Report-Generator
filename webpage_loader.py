from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import date
import time
from requests import Request, Session

from Settings_Data import SettingsData
from table_data import TableData
from utils import type_check
from webpage_data import WebpageData


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
        self.driver = None
        self.waybill_data = None
        self.webpage_data = WebpageData()

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

    def check_element_loaded(self, element: str, wait_time: int) -> bool:
        """Check if a element is loaded or not.

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

        return self.check_element_loaded(element="//div[@class='DlinkLoggedIn']//a[normalize-space()='Logout']",
                                         wait_time=2)

    def login(self):
        """
        Allows the script to log in to the Cargo Webpage.

        The method allows the script to get the XPATH for the username and password fields. It then inputs the username
        and password attributes and sends the keys to the webpage, which allows it to login. It gets the username
        and password from the WebpageData class.

        :return: None
        """
        username_field = self.driver.find_element(By.XPATH, "//input[@id='UserName']")
        username_field.send_keys(self.webpage_data.get_username())

        password_field = self.driver.find_element(By.XPATH, "//input[@id='pwd']")
        password_field.send_keys(self.webpage_data.get_password())

        login_button = self.driver.find_element(By.XPATH, "//button[@id='load2']")
        login_button.click()

    # TODO: Add docstring when method is finished.
    def waybills_to_ship_page(self, url: str) -> bool:
        self.load_url(url)
        if self.check_element_loaded("//input[@id='txt_from_date75']", wait_time=5):
            return True
        return False

    # TODO: Add docstring when method is finished.
    def fill_in_waybills_form(self):
        from_date_field = self.driver.find_element(By.XPATH, "//input[@id='txt_from_date75']")
        from_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                                "4]/div/div[2]/div/select")
        to_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]/div/div/div/div["
                                                              "5]/div/div[2]/div/select")
        search_button = self.driver.find_element(By.XPATH, "//button[@id='btn_search75']")

        # Get Setting Values for SLA/Bot Settings to fill in form with appropriate settings.
        sla_bot_data = self.webpage_data.get_setting_values("SLA")

        # Clear the date field, or it will cause issues inputting the date.
        from_date_field.clear()

        from_date_field.send_keys(sla_bot_data["Date"])
        Select(from_airport_field).select_by_value(sla_bot_data["FromAirport"])
        Select(to_airport_field).select_by_value(sla_bot_data["ToAirport"])

        search_button.click()

        sort_button = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((
                By.XPATH, "/html/body/div[7]/div[5]/div[3]/div[1]/div[2]/div/div[3]/div/table/thead/tr/th[13]/a")))
        sort_button.click()

        # Find Table
        waybill_table = self.driver.find_element(By.XPATH,
                                                 "/html/body/div[7]/div[5]/div[3]/div[1]/div[2]/div/div[4]/table")

        # Get Entire HTML Code for table element.
        waybill_html = waybill_table.get_attribute('outerHTML')

        self.quit_selenium()

        return waybill_html, sla_bot_data["DayAmount"]

    def search_awbs(self, url: str) -> bool:
        self.load_url(url)
        if self.check_element_loaded("//input[@id='txt_key']", wait_time=5):
            return True
        return False

    def fill_in_search_form(self):
        from_date_field = self.driver.find_element(By.XPATH, "//input[@id='txt_date_range_from']")
        to_date_field = self.driver.find_element(By.XPATH, "//input[@id='txt_date_range_to']")
        from_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]"
                                                                "/div/div/div[1]/div[3]/div/div[2]/div/select")
        to_airport_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]"
                                                              "/div/div/div[2]/div[2]/div/div[2]/div/select")
        keyword_field = self.driver.find_element(By.XPATH, "//input[@id='txt_key']")
        search_button = self.driver.find_element(By.XPATH, "//button[@id='btn_search']")

        home_delivery_data = self.webpage_data.get_setting_values("Home")

        from_date_field.send_keys(home_delivery_data["Date"])
        Select(from_airport_field).select_by_value(home_delivery_data["FromAirport"])
        Select(to_airport_field).select_by_value(home_delivery_data["ToAirport"])
        keyword_field.send_keys(home_delivery_data["Keyword"])

        search_button.click()

        if self.results_found():
            # Allows the hidden dropdown box to appear.
            time.sleep(1)
            items_per_page_drop_down = self.driver.find_element(By.XPATH,
                                                                "/html/body/div[7]/div[5]/div[2]/div/div[2]/span["
                                                                "1]/span/select")

            self.driver.execute_script("arguments[0].style.display = 'block';", items_per_page_drop_down)

            Select(items_per_page_drop_down).select_by_value('all')

            # Find Table
            waybill_table = self.driver.find_element(By.XPATH,
                                                     "/html/body/div[7]/div[5]/div[2]/div/table")

            # Get Entire HTML Code for table element.
            waybill_html = waybill_table.get_attribute('outerHTML')

            return waybill_html

        else:
            print("Failed")

    def results_found(self):
        return self.check_element_loaded(element="/html/body/div[7]/div[5]/div[2]/div/table", wait_time=3)