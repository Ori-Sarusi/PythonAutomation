from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class AuthPage(BasePage):
    """
    Page Object Model for the Authentication screen (Login & Register).
    Encapsulates locators and user actions for both forms.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Tabs using get_by_role
        self.tab_login: Locator = page.get_by_role("button", name="Login")
        self.tab_register: Locator = page.get_by_role("button", name="Register")

        # Login Form Elements (using built-in role / id / placeholder locators)
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
        self.tab_login.click()

    def switch_to_register_tab(self):
        self.tab_register.click()

    # --- Actions: Login Flow ---
    def fill_username(self, username: str):
        self.username_input.fill(username)

    def fill_password(self, password: str):
        self.password_input.fill(password)

    def click_login(self):
        self.login_button.click()

    def login(self, username: str, password: str):
        """High-level action to perform complete login."""
        self.fill_username(username)
        self.fill_password(password)
        self.click_login()

    # --- Actions: Registration Flow ---
    def register(self, username: str, email: str, password: str, confirm_password: str):
        """High-level action to perform complete user registration."""
        self.switch_to_register_tab()
        self.reg_username_input.fill(username)
        self.reg_email_input.fill(email)
        self.reg_password_input.fill(password)
        self.reg_confirm_password_input.fill(confirm_password)
        self.register_button.click()
