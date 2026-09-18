import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import AmazonHomePage
from pages.search_result_page import AmazonSearchResultPage

@pytest.mark.parametrize("item", [
    "nike air max",
    "reebok crossfit shoes men",
    "puma sneakers",
    "adidas classic shoes"
])
@pytest.mark.regressiontest
def test_search_multiple_items(browser: WebDriver, item: str) -> None:
    """Verify search functionality for multiple items using parametrization."""
    home_page = AmazonHomePage(browser)
    search_result_page = AmazonSearchResultPage(browser)

    # Navigate to home page and verify
    home_page.load_page()
    home_page.verify_title()

    # Search for item
    home_page.search_item(item)

    # Verify search results page title
    search_result_page.verify_title(item)