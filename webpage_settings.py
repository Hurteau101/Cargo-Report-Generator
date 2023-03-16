from selenium import webdriver
import os


class WebpageSettings:
    def __init__(self, options=None):
        if options is None:
            self.driver = webdriver.Chrome("chromedriver.exe")
        else:
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
            # self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            self.driver = webdriver.Chrome("chromedriver.exe", options=options)

    # Return the webdriver object. This way you can pass it as an argument, to create a headless chrome.
    classmethod

    def headless_chrome(cls):
        """Call this method to allow headless mode."""
        return webdriver.ChromeOptions()
