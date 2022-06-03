from selenium import webdriver


class WebDriver:
    def __init__(self):
        self.options = webdriver.ChromeOptions()

    def add_option(self, option):
        self.options.add_argument(option)

    def add_options(self, options):
        for option in options:
            self.options.add_argument(option)

    def create_driver(self):
        return webdriver.Chrome('../resources/chromedriver.exe', options=self.options)

