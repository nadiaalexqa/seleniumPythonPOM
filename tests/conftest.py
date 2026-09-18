import allure
import pytest
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from typing import Generator


# CLI options: pytest --browser=firefox --headless
def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--browser", action="store", default="chrome", help="Browser to run tests: chrome or firefox"
    )
    parser.addoption(
        "--headless", action="store_true", default=False, help="Run browser in headless mode"
    )


# check if a test failed (needed for conditional screenshots)
@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


@pytest.fixture()
def browser(request: pytest.FixtureRequest) -> Generator[webdriver.Remote, None, None]:
    browser_name = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    driver: webdriver.Remote

    # Cross-browser support
    if browser_name.lower() == "chrome":
        options = ChromeOptions()

        # --- NEW: REQUIRED FOR GITHUB ACTIONS (Docker) ---
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        # --- NEW: STEALTH OPTIONS TO BYPASS BOT DETECTION ---
        # 1. Hide the fact that Selenium is controlling the browser
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # 2. Spoof the User-Agent to look like a real Windows Chrome user
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        )
        # ---------------------------------------------------

        # --- ORIGINAL LOGIC ---
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(options=options)
        # ----------------------

    elif browser_name.lower() == "firefox":
        # --- ORIGINAL LOGIC ---
        options = FirefoxOptions()
        if headless:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
        # ----------------------
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    # --- MODIFIED: Only maximize if not headless ---
    if not headless:
        driver.maximize_window()
    # -----------------------------------------------

    yield driver

    # --- ORIGINAL LOGIC: Only attach screenshot if the test FAILED ---
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        allure.attach(
            driver.get_screenshot_as_png(),
            name=f"Failure_Screenshot_{browser_name}",
            attachment_type=AttachmentType.PNG,
        )
        # Attach browser logs on failure
        try:
            log = "".join([f"{entry['level']}: {entry['message']}\n" for entry in driver.get_log('browser')])
            allure.attach(log, name="Browser_Console_Logs", attachment_type=AttachmentType.TEXT)
        except Exception:
            pass  # Firefox doesn't support get_log('browser') the same way
    # -------------------------------------------------------------------

    # When test is done, close ALL windows of the browser
    driver.quit()