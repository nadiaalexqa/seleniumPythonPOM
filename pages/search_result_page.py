from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class AmazonSearchResultPage(BasePage):
    """Page Object representing the Amazon search results page."""

    # Element Locators
    SEARCH_FIELD = (By.ID, "twotabsearchtextbox")
    SEARCH_BUTTON = (By.XPATH, "//input[@value='Go']")

    def search_item(self, item: str) -> None:
        """Search for an item from the results page."""
        search_input = self.wait.until(EC.visibility_of_element_located(self.SEARCH_FIELD))
        search_input.clear()
        search_input.send_keys(item + Keys.RETURN)

    def verify_title(self, item: str) -> None:
        """Verify that the page title contains the searched item."""
        # Wait until the title contains the item to avoid race conditions
        self.wait.until(EC.title_contains(item))
        actual_title = self.browser.title

        # Robust assertion: use 'in' instead of '=='
        assert item.lower() in actual_title.lower(), \
            f"Expected '{item}' in title, but got '{actual_title}'"