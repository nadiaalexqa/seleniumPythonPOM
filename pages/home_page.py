"""
Page Object for the Amazon Home Page.
Encapsulates locators and interactions for the Amazon landing page.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from typing import Tuple
from pages.base_page import BasePage

class AmazonHomePage(BasePage):
    """Page Object representing the Amazon home page."""

    # URL and expected title keyword
    URL: str = 'https://www.amazon.com'
    TITLE_KEYWORD: str = 'Amazon'

    # Element Locators
    SEARCH_FIELD: Tuple[By, str] = (By.ID, "twotabsearchtextbox")
    BOT_CONTINUE_BUTTON: Tuple[By, str] = (By.XPATH, "//button[contains(., 'Continue shopping')]")

    def load_page(self) -> None:
        """Navigate to the Amazon home page and handle bot detection."""
        self.browser.get(self.URL)
        self._handle_bot_detection()

    def _handle_bot_detection(self) -> None:
        """
        Check if Amazon's bot detection screen is present.
        If so, click the 'Continue shopping' button to proceed.
        """
        try:
            # Wait up to 3 seconds to see if the bot detection button appears
            bot_button = self.wait.until(
                EC.element_to_be_clickable(self.BOT_CONTINUE_BUTTON)
            )
            bot_button.click()

            # After clicking, wait for the real search field to appear
            self.wait.until(
                EC.visibility_of_element_located(self.SEARCH_FIELD)
            )
        except TimeoutException:
            # The bot screen was not present, which is the normal case.
            # Continue as usual.
            pass

    def verify_title(self) -> None:
        """
        Verify the page title contains the expected keyword.
        Uses an explicit wait to handle dynamic page loading.
        """
        self.wait.until(EC.title_contains(self.TITLE_KEYWORD))

        actual_title = self.browser.title
        assert self.TITLE_KEYWORD in actual_title, \
            f"Expected title to contain '{self.TITLE_KEYWORD}', but got '{actual_title}'"

    def search_item(self, item: str) -> None:
        """Search for an item on Amazon."""
        search_input = self.wait.until(
            EC.visibility_of_element_located(self.SEARCH_FIELD)
        )
        search_input.clear()
        search_input.send_keys(item + Keys.RETURN)