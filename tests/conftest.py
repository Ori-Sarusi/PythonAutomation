import pytest
from playwright.sync_api import Page
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage

@pytest.fixture
def auth_page(page: Page) -> AuthPage:
    """Fixture providing an AuthPage instance bound to the active Playwright page."""
    return AuthPage(page)

@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    """Fixture providing a CatalogPage instance bound to the active Playwright page."""
    return CatalogPage(page)
