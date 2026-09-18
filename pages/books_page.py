from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage

class BooksPage(BasePage):
    """Page Object representing the Amazon Books page."""

    BASE_BOOKS_URL = "https://www.amazon.com/books-used-books-textbooks/b/?ie=UTF8&node=283155&ref_=nav_cs_books_2ed85a0fb54a4598ba909c22690d166e"
    PAGE_TITLE_KEYWORD = "Books"

    # Element Locators
    BEST_BOOKS_BUTTON = (By.XPATH, "//a[@aria-label='Best books of the month']")
    CELEBRITY_PICKS_BUTTON = (By.XPATH, "//a[@aria-label='Celebrity Picks']")

    def navigate_to_books_page(self) -> None:
        """Navigate to the Books page."""
        self.browser.get(self.BASE_BOOKS_URL)

    def verify_title(self) -> None:
        """Verify the Books page title loads correctly."""
        self.wait.until(EC.title_contains(self.PAGE_TITLE_KEYWORD))
        actual_title = self.browser.title
        assert self.PAGE_TITLE_KEYWORD in actual_title, \
            f"Expected '{self.PAGE_TITLE_KEYWORD}' in title, but got '{actual_title}'"

    def click_best_books(self) -> None:
        """Click the 'Best books of the month' button."""
        button = self.wait.until(EC.element_to_be_clickable(self.BEST_BOOKS_BUTTON))
        button.click()