from selenium import webdriver
import os


class WebpageSettings:
    """
    A collection of commonly used settings for Selenium webdriver.

      Methods:
        - headless_chrome: Sets Selenium Webdriver into headless mode.
    """
    @staticmethod
    def headless_chrome() -> webdriver.ChromeOptions:
        """
        Returns a set of options for running Chrome in headless mode.

        The returned options include a user-agent string, log level settings, SSL certificate and error
        handling options, and experimental options for downloading files to a default directory without
        prompting the user.

        :return: An instance of the ChromeOptions class with the specified settings.

        """
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, "
                             "like Gecko) Chrome/58.0.3029.110 Safari/537.3")
        options.add_argument('log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        # Prevent detection from Selenium, so website doesn't block the request
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("prefs", {
            "download.default_directory": os.path.expanduser('~\Downloads'),
            "download.prompt_for_download": False,
        })
        return options
