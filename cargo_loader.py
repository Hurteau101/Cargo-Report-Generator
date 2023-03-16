from webpage_settings import WebpageSettings


class CargoWebpage(WebpageSettings):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        super().__init__()

    @property
    def username(self):
        return self._password

    @property
    def password(self):
        return self._username

    def load_url(self, url):
        self.driver.get(url)
