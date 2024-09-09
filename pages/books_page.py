from selenium.webdriver.common.by import By


class BooksPage:

    # constructor
    def __init__(self, browser):
        self.browser = browser

    BASE_BOOKS_URL = "https://www.amazon.com/books-used-books-textbooks/b/?ie=UTF8&node=283155&ref_=nav_cs_books_2ed85a0fb54a4598ba909c22690d166e"
    PAGE_TITLE = "Amazon.com: Books"

    BEST_BOOKS_BUTTON = (By.XPATH, "//a[@aria-label='Best books of the month']")
    CELEBRITY_PICKS_BUTTON = (By.XPATH, "//a[@aria-label='Celebrity Picks']")

    def navigate_to_books_page(self):
        self.browser.get(self.BASE_BOOKS_URL)

    def assert_books_page_title(self):
        assert self.browser.title == self.PAGE_TITLE