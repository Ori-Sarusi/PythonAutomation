from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class AuthPage(BasePage):
    """
    Page Object Model for Authentication (Login & Register) with step-by-step logging.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Tabs
        self.tab_login: Locator = page.get_by_role("button", name="Login")
        self.tab_register: Locator = page.get_by_role("button", name="Register")

        # Login Form Elements
        self.username_input: Locator = page.locator("#username")
        self.password_input: Locator = page.locator("#password")
        self.login_button: Locator = page.locator("#login-form").get_by_role("button", name="Login")
        self.login_error: Locator = page.locator("#login-error")

        # Register Form Elements
        self.reg_username_input: Locator = page.locator("#reg-username")
        self.reg_email_input: Locator = page.locator("#reg-email")
        self.reg_password_input: Locator = page.locator("#reg-password")
        self.reg_confirm_password_input: Locator = page.locator("#reg-confirm-password")
        self.register_button: Locator = page.get_by_role("button", name="Create Account")
        self.register_error: Locator = page.locator("#register-error")
        self.register_success: Locator = page.locator("#register-success")

    # --- Actions: Tab Navigation ---
    def switch_to_login_tab(self):
        self.click(self.tab_login, "Login Tab")

    def switch_to_register_tab(self):
        self.click(self.tab_register, "Register Tab")

    # --- Actions: Login Flow ---
    def fill_username(self, username: str):
        self.fill(self.username_input, username, "Username Input")

    def fill_password(self, password: str):
        self.fill(self.password_input, password, "Password Input")

    def click_login(self):
        self.click(self.login_button, "Login Submit Button")

    def login(self, username: str, password: str):
        """High-level action to perform complete login with logging."""
        self.logger.info(f"Initiating login sequence for user: {username}")
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    # --- Actions: Registration Flow ---
    def register(self, username: str, email: str, password: str, confirm_password: str):
        """High-level action to perform complete user registration with logging."""
        self.logger.info(f"Initiating registration sequence for: {username} ({email})")
        self.switch_to_register_tab()
        self.fill(self.reg_username_input, username, "Reg Username")
        self.fill(self.reg_email_input, email, "Reg Email")
        self.fill(self.reg_password_input, password, "Reg Password")
        self.fill(self.reg_confirm_password_input, confirm_password, "Reg Confirm Password")
        self.click(self.register_button, "Create Account Button")

    def get_email_validation_message(self) -> str:
        """Returns the native HTML5 validation message from the browser tooltip."""
        msg = self.reg_email_input.evaluate("el => el.validationMessage")
        self.logger.info(f"Email field validation message: '{msg}'")
        return msg

    def is_email_valid(self) -> bool:
        """Checks if the email input passes native browser validation."""
        valid = self.reg_email_input.evaluate("el => el.checkValidity()")
        self.logger.info(f"Email field validity state: {valid}")
        return valid
