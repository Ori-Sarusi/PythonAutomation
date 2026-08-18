import pytest
from playwright.sync_api import expect
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from config import config

class TestAuth:
    """
    Test suite for Authentication (Login and Registration) flows.
    Follows the AAA (Arrange, Act, Assert) pattern with full Page Object encapsulation.
    """

    def test_successful_login(self, auth_page: AuthPage, catalog_page: CatalogPage):
        # 1. Arrange
        auth_page.navigate(config.BASE_URL)

        # 2. Act
        auth_page.login(config.STANDARD_USER, config.PASSWORD)

        # 3. Assert: Verify through CatalogPage object without raw locators in test
        expect(catalog_page.products_grid).to_be_visible()
        expect(catalog_page.user_display).to_have_text(config.STANDARD_USER)

    def test_locked_out_user_login(self, auth_page: AuthPage):
        # 1. Arrange
        auth_page.navigate(config.BASE_URL)

        # 2. Act
        auth_page.login(config.LOCKED_OUT_USER, config.PASSWORD)

        # 3. Assert: Error banner is shown with locked out message
        expect(auth_page.login_error).to_be_visible()
        expect(auth_page.login_error).to_contain_text("Epic sadface: Sorry, this user has been locked out.")

    def test_invalid_password_login(self, auth_page: AuthPage):
        # 1. Arrange
        auth_page.navigate(config.BASE_URL)

        # 2. Act
        auth_page.login(config.STANDARD_USER, "wrong_password_123")

        # 3. Assert: Error message for invalid credentials
        expect(auth_page.login_error).to_be_visible()
        expect(auth_page.login_error).to_have_text("Invalid username or password.")

    def test_successful_registration(self, auth_page: AuthPage):
        # 1. Arrange
        auth_page.navigate(config.BASE_URL)

        # 2. Act
        auth_page.register(
            username="new_tester_user",
            email="tester@example.com",
            password="securePass123",
            confirm_password="securePass123"
        )

        # 3. Assert: Registration success alert
        expect(auth_page.register_success).to_be_visible()
        expect(auth_page.register_success).to_contain_text("Account created successfully!")

    def test_registration_password_mismatch(self, auth_page: AuthPage):
        # 1. Arrange
        auth_page.navigate(config.BASE_URL)

        # 2. Act
        auth_page.register(
            username="mismatch_user",
            email="mismatch@example.com",
            password="password123",
            confirm_password="password_diff"
        )

        # 3. Assert: Passwords do not match error
        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Passwords do not match.")
