from playwright.sync_api import Page, Locator
from utils.logger import get_logger

class BasePage:
    """
    BasePage serves as the parent class for all Page Objects in the framework.
    It encapsulates common browser interactions, step logging, and holds the Playwright Page instance.
    """
    def __init__(self, page: Page):
        self.page = page
        self.logger = get_logger(self.__class__.__name__)

    def navigate(self, url: str):
        """Navigate to a given URL with step logging."""
        self.logger.info(f"Navigating to URL: {url}")
        self.page.goto(url)

    def click(self, locator: Locator, element_name: str = "Element"):
        """Click an element with step logging."""
        self.logger.info(f"Clicking on: {element_name}")
        locator.click()

    def fill(self, locator: Locator, value: str, field_name: str = "Field"):
        """Fill an input field with step logging."""
        display_val = "••••••" if "password" in field_name.lower() else value
        self.logger.info(f"Filling '{field_name}' with: {display_val}")
        locator.fill(value)

    def get_title(self) -> str:
        """Return the current document title."""
        title = self.page.title()
        self.logger.info(f"Retrieved page title: '{title}'")
        return title

    def get_url(self) -> str:
        """Return the current URL."""
        url = self.page.url
        self.logger.info(f"Retrieved current URL: '{url}'")
        return url
