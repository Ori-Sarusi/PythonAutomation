from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CatalogPage(BasePage):
    """
    Page Object Model for the Catalog/Products screen and top navigation.
    """
    def __init__(self, page: Page):
        super().__init__(page)
        
        # Navigation & User info
        self.user_display: Locator = page.locator("#username-val")
        self.logout_button: Locator = page.locator("#logout-btn")
        self.cart_button: Locator = page.locator("#cart-btn")
        self.cart_count_badge: Locator = page.locator("#cart-count")

        # Products controls & grid
        self.search_input: Locator = page.locator("#search-input")
        self.category_filter: Locator = page.locator("#category-filter")
        self.sort_select: Locator = page.locator("#sort-select")
        self.products_grid: Locator = page.locator("#products-grid")

    def get_logged_in_username(self) -> str:
        return self.user_display.inner_text()

    def search_product(self, product_name: str):
        self.search_input.fill(product_name)

    def filter_by_category(self, category: str):
        self.category_filter.select_option(category)

    def sort_by(self, sort_value: str):
        self.logger.info(f"Sorting products by: '{sort_value}'")
        self.sort_select.select_option(sort_value)

    def get_all_product_titles(self) -> list[str]:
        """Returns a list of all product title strings currently displayed."""
        titles = self.page.locator("[data-test='product-title']").all_inner_texts()
        self.logger.info(f"Retrieved {len(titles)} product titles: {titles}")
        return titles

    def get_all_product_prices(self) -> list[float]:
        """Returns a list of all product prices as floats (stripped of '$')."""
        price_texts = self.page.locator("[data-test='product-price']").all_inner_texts()
        prices = [float(p.replace("$", "").strip()) for p in price_texts]
        self.logger.info(f"Retrieved {len(prices)} product prices: {prices}")
        return prices

    def add_to_cart(self, product_id: int):
        self.page.locator(f"[data-test='add-to-cart-{product_id}']").click()

    def open_cart(self):
        self.cart_button.click()

    def logout(self):
        self.logout_button.click()
