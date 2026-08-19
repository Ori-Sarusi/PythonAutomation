from playwright.sync_api import Page, Locator

class BasePage:
    """
    BasePage serves as the parent class for all Page Objects in the framework.
    It encapsulates common browser interactions and holds the Playwright Page instance.
    """
    def __init__(self, page: Page):
        self.page = page

    def navigate(self, url: str):
        """Navigate to a given URL."""
        self.page.goto(url)

    def get_title(self) -> str:
        """Return the current document title."""
        return self.page.title()

    def get_url(self) -> str:
        """Return the current URL."""
        return self.page.url
