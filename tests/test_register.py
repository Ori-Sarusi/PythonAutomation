import pytest
from playwright.sync_api import expect
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from config import config

class TestRegister:
    # -------------------------------------------------------------
    # 1. POSITIVE TESTS (Happy Paths & End-to-End User Journeys)
    # -------------------------------------------------------------
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

    def test_register_and_login_flow(self, auth_page: AuthPage, catalog_page: CatalogPage):
        """End-to-end: Register a brand new user, switch to login tab, and log in with new credentials."""
        new_username = "journey_user"
        new_password = "password123"
        new_email = "journey@example.com"

        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username=new_username,
            email=new_email,
            password=new_password,
            confirm_password=new_password
        )

        expect(auth_page.register_success).to_be_visible()

        # Switch to Login tab and perform login with newly created account
        auth_page.switch_to_login_tab()
        auth_page.login(new_username, new_password)

        expect(catalog_page.user_display).to_have_text(new_username)

    # -------------------------------------------------------------
    # 2. NEGATIVE TESTS (Field Validations & Error Messages)
    # -------------------------------------------------------------
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

    def test_registration_duplicate_username(self, auth_page: AuthPage):
        """Registering with an already existing username should be rejected."""
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username=config.STANDARD_USER,
            email="duplicate@example.com",
            password="securePassword123",
            confirm_password="securePassword123"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Username already exists.")

    @pytest.mark.parametrize("invalid_email", [
        "plainaddress",
        "missingatsign.com",
        "username@",
        "@missingusername.com"
    ])
    def test_registration_invalid_email_formats(self, auth_page: AuthPage, invalid_email: str):
        """Validates that browser rejects malformed emails and displays native validation tooltip."""
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username=f"user_{invalid_email.replace('@', '_').replace('.', '_')}",
            email=invalid_email,
            password="validPassword123",
            confirm_password="validPassword123"
        )

        assert not auth_page.is_email_valid(), f"Email '{invalid_email}' was unexpectedly considered valid!"
        validation_message = auth_page.get_email_validation_message()
        assert len(validation_message) > 0, "Expected a browser validation message tooltip, but got none."

    # -------------------------------------------------------------
    # 3. EDGE CASES (Special Characters, Whitespaces, Boundary Lengths)
    # -------------------------------------------------------------
    def test_registration_whitespace_only_username(self, auth_page: AuthPage):
        """Usernames with only spaces should be rejected."""
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username="   ",
            email="spaces@example.com",
            password="securePassword123",
            confirm_password="securePassword123"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Username cannot be empty or blank spaces.")

    def test_registration_xss_injection_in_username(self, auth_page: AuthPage):
        """Security edge case: ensure HTML / Script tag injections in username are safely handled."""
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username="<script>alert('xss')</script>",
            email="xss@example.com",
            password="securePassword123",
            confirm_password="securePassword123"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Username contains invalid characters.")

    def test_registration_excessive_length_inputs(self, auth_page: AuthPage):
        """Boundary test: 500+ character username should be rejected."""
        excessive_username = "a" * 501
        auth_page.navigate(config.BASE_URL)
        auth_page.register(
            username=excessive_username,
            email="toolong@example.com",
            password="securePassword123",
            confirm_password="securePassword123"
        )

        expect(auth_page.register_error).to_be_visible()
        expect(auth_page.register_error).to_have_text("Username exceeds maximum allowed length.")
