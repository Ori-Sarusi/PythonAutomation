from playwright.sync_api import expect
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from config import config

class TestLogin:
    # --- Positive Tests ---
    def test_successful_login(self, auth_page: AuthPage, catalog_page: CatalogPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.login(config.STANDARD_USER, config.PASSWORD)

        expect(catalog_page.products_grid).to_be_visible()
        expect(catalog_page.user_display).to_have_text(config.STANDARD_USER)

    # --- Negative Tests ---
    def test_locked_out_user_login(self, auth_page: AuthPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.login(config.LOCKED_OUT_USER, config.PASSWORD)

        expect(auth_page.login_error).to_be_visible()
        expect(auth_page.login_error).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

    def test_invalid_password_login(self, auth_page: AuthPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.login(config.STANDARD_USER, "wrong_password_123")

        expect(auth_page.login_error).to_be_visible()
        expect(auth_page.login_error).to_have_text("Invalid username or password.")
