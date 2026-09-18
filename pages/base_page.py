from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait


class BasePage:
    """Base class for all Page Objects. Handles driver setup and common waits."""

    def __init__(self, browser: WebDriver):
        self.browser = browser
        self.wait = WebDriverWait(browser, 10)