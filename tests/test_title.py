import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from pages.home_page import AmazonHomePage

@pytest.mark.smoketest
def test_amazon_title(browser: WebDriver) -> None:
    """Verify that the Amazon home page title is correct."""
    home_page = AmazonHomePage(browser)

    # Navigate to Amazon home page
    home_page.load_page()

    # Verify Amazon home page title contains expected keyword
    home_page.verify_title()