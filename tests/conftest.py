import pytest
from playwright.sync_api import Page, BrowserContext
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from utils.logger import get_logger

logger = get_logger("TestSetup")

# -------------------------------------------------------------
# 1. TEST SUITE LIFECYCLE (Before All / After All)
# -------------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def test_suite_setup():
    """Executes once before all tests in the test suite run."""
    logger.info("==================================================")
    logger.info("🚀 Starting Test Automation Suite Execution")
    logger.info("==================================================")
    yield
    logger.info("==================================================")
    logger.info("🏁 Finished Test Automation Suite Execution")
    logger.info("==================================================")

# -------------------------------------------------------------
# 2. TEST CASE LIFECYCLE (Before Each / After Each)
# -------------------------------------------------------------
@pytest.fixture(scope="function", autouse=True)
def test_case_setup_teardown(request):
    """Executes before and after EACH test function."""
    test_name = request.node.name
    logger.info(f"▶️ Starting Test: '{test_name}'")
    yield
    logger.info(f"⏹️ Finished Test: '{test_name}'")

# -------------------------------------------------------------
# 3. PAGE OBJECT FIXTURES
# -------------------------------------------------------------
@pytest.fixture
def auth_page(page: Page) -> AuthPage:
    """Fixture providing an AuthPage instance with step-by-step logging."""
    return AuthPage(page)

@pytest.fixture
def catalog_page(page: Page) -> CatalogPage:
    """Fixture providing a CatalogPage instance with step-by-step logging."""
    return CatalogPage(page)
