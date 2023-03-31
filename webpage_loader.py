from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import requests
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
        return self.driver.get_cookies()

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

    def check_search_awbs_page(self, url: str) -> bool:
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
            # Allows the hidden dropdown box to appear by waiting 1 second.
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

    def search_awb(self, awb_list: list):
        """
        Method will load the search AWB page. It will loop through the list of AWB's passed in as an argument (List of
        dictionarys of AWB's). It will then check if it finds certain text on the AWB Pop Up Modal Page.
        If it does it will add the Flight information to that specific dictionary in the awb_info list. If it doesn't
        it will remove that dictionary of that awb from awb_info list. Returns the list of home delivery AWB's.
        :param awb_list: List of dictionarys that contain AWB's.
        :return: List of dictionarys that are the Home Delivery AWB's.
        """
        self.load_url(self.webpage_data.get_search_awb_url())
        awb_field = self.driver.find_element(By.XPATH, "/html/body/div[7]/form/div/div[1]"
                                                       "/div/div/div[1]/div[1]/div/div[2]/input")
        close_awb_modal = self.driver.find_element(By.XPATH, "/html/body/div[7]/div[6]/div/div/div[1]/button")
        search_button = self.driver.find_element(By.XPATH, "//button[@id='btn_search']")

        awb_info = awb_list.copy()

        for i in reversed(range(len(awb_list))):
            awb = awb_list[i].get("AWB No.")

            awb_field.send_keys(awb)
            search_button.click()
            if self.check_home_delivery_text():
                awb_info[i].update(self.get_status_of_awb())
            else:
                awb_info.pop(i)
            close_awb_modal.click()
            awb_field.clear()

        self.quit_selenium()

        return awb_info

    def check_home_delivery_text(self):
        """
        Check if "Home Delivery" text is located on the AWB Page. If it is return true, otherwise return False
        :return: True if "Home Delivery" text found | False if "Home Delivery" NOT found.
        """
        if self.check_element_loaded("/html/body/div[7]/div[6]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div[3]",
                                     wait_time=5):
            awb_page = self.driver.find_element(By.XPATH, "/html/body/div[7]/div[6]/div/div/div[2]/div/div/div[2]")

            if "HOME DELIVERY" in awb_page.text:
                return True
            return False

    def get_status_of_awb(self):
        """
        Check if the AWB has been shipped or if it's waiting to be shipped. There is a Try/Except block, in the off
        chance an AWB was created inproperly. If an AWB is created inproperly, it will get the status message of that
        AWB and return it back to specific awb dictionary. If there is no error, it will obtain the shipped flight
        information about that AWB and return it back to that AWB.
        :return: Returns a dictionary of flight information or status information (if AWB isn't created properly).
        """
        try:
            table = self.driver.find_element(By.XPATH, "/html/body/div[7]/div[6]/div/div/div[2]"
                                                   "/div/div/div[2]/div/div/div[2]/div[10]/div/div[2]/div/table")
        except NoSuchElementException:
            return self.awb_status_not_found()
        else:
            rows = table.find_elements(By.TAG_NAME, "tr")
            row = rows[-1]

            cells = row.find_elements(By.TAG_NAME, "td")
            cell_list = [cell.text for cell in cells]

            row_header = table.find_elements(By.TAG_NAME, "th")
            row_header_list = [row.text for row in row_header]

            status_dict = {row_header_list[i]: cell_list[i] for i in range(len(row_header_list))
                           if row_header_list[i] in ['Flight Status', 'Flight Number', 'Flight Date']}

            return status_dict

    def awb_status_not_found(self):
        """
        If AWB is created incorrectly, this method is called and will find the status information about the AWB and
        return it as a dictionary.
        :return: Returns a dictionary about the status information of the AWB.
        """
        table = self.driver.find_element(By.XPATH, "/html/body/div[7]/div[6]/div/div/div[2]"
                                              "/div/div/div[2]/div/div/div[2]/div[8]/div/div[2]/div/table")
        rows = table.find_elements(By.TAG_NAME, "tr")
        last_row = rows[-1]
        last_cell = last_row.find_elements(By.TAG_NAME, "td")

        status_dict = {"Flight Status": last_cell[-1].text}

        return status_dict

    def results_found(self):
        """
        Calls the check_element_loaded to see if the AWB Pop Up Modal is properly loaded before trying to locate text.
        It will wait 5 seconds before returning False.
        :return: Returns True if it can find the table in the AWB Pop Up Modal otherwise False if it can't.
        """
        return self.check_element_loaded(element="/html/body/div[7]/div[5]/div[2]/div/table", wait_time=3)