from webpage_settings import WebpageSettings
from selenium.webdriver.chrome.service import Service
from selenium import webdriver


class CargoWebpage:
    def __init__(self, options=None):
        self._username = None
        self._password = None
        service = Service("chromedriver.exe")
        self.driver = webdriver.Chrome(service=service, options=options)


    @property
    def username(self):
        return self._password
    @username.setter
    def username(self, username):
        self._username = username

    @property
    def password(self):
        return self._username

    @password.setter
    def password(self, password):
        self._password = password

    def load_url(self, url):
        self.driver.get(url)

