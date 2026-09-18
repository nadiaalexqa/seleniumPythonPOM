import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import AmazonHomePage
from pages.search_result_page import AmazonSearchResultPage

@pytest.mark.regressiontest
def test_search_airmax(browser: WebDriver) -> None:
    """Verify that searching for 'nike air max' returns the correct title."""
    home_page = AmazonHomePage(browser)
    search_result_page = AmazonSearchResultPage(browser)
    search_item = 'nike air max'

    # Navigate to home page and verify
    home_page.load_page()
    home_page.verify_title()

    # Search for item
    home_page.search_item(search_item)

    # Verify search results page title
    search_result_page.verify_title(search_item)