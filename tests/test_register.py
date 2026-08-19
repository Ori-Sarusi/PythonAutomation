from playwright.sync_api import expect
from pages.auth_page import AuthPage
from config import config

class TestRegister:
    # --- Positive Tests ---
    def test_successful_registration(self, auth_page: AuthPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username="new_tester_user",
            email="tester@example.com",
            password="securePass123",
            confirm_password="securePass123"
        )

        expect(auth_page.register_success).to_be_visible()
        expect(auth_page.register_success).to_contain_text("Account created successfully!")

    # --- Negative Tests ---
    def test_registration_password_mismatch(self, auth_page: AuthPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username="mismatch_user",
            email="mismatch@example.com",
            password="password123",
            confirm_password="password_diff"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Passwords do not match.")

    def test_registration_short_password(self, auth_page: AuthPage):
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username="short_pwd_user",
            email="short@example.com",
            password="123",
            confirm_password="123"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Password must be at least 6 characters long.")
