"""
Page Object for the Amazon Home Page.
Encapsulates locators and interactions for the Amazon landing page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple
from pages.base_page import BasePage

class AmazonHomePage(BasePage):
    """Page Object representing the Amazon home page."""

    # URL and expected title keyword
    URL: str = 'https://www.amazon.com'
    TITLE_KEYWORD: str = 'Amazon'

    # Element Locators
    SEARCH_FIELD: Tuple[By, str] = (By.ID, "twotabsearchtextbox")

    # Note: __init__ is inherited from BasePage.
    # It automatically sets self.browser and self.wait.

    def load_page(self) -> None:
        """Navigate to the Amazon home page."""
        self.browser.get(self.URL)

    def verify_title(self) -> None:
        """
        Verify the page title contains the expected keyword.
        Uses an explicit wait to handle dynamic page loading.
        """
        # Wait until the title contains the keyword before asserting
        self.wait.until(EC.title_contains(self.TITLE_KEYWORD))

        actual_title = self.browser.title
        assert self.TITLE_KEYWORD in actual_title, \
            f"Expected title to contain '{self.TITLE_KEYWORD}', but got '{actual_title}'"

    def search_item(self, item: str) -> None:
        """Search for an item on Amazon."""
        # Explicit wait for element to be visible before interacting
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_FIELD)
        )
        search_input.clear()
        search_input.send_keys(item + Keys.RETURN)