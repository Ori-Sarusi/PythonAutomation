from playwright.sync_api import Page, Locator
from pages.base_page import BasePage

class CartPage(BasePage):
    """
    Page Object Model for the Shopping Cart screen.
    """
    def __init__(self, page: Page):
        super().__init__(page)

        self.cart_section: Locator = page.locator("#cart-section")
        self.cart_items_container: Locator = page.locator("#cart-items")
        self.cart_rows: Locator = page.locator("[data-test='cart-row']")
        self.close_cart_button: Locator = page.locator("#close-cart-btn")

        # Coupon & Pricing Summary
        self.coupon_input: Locator = page.locator("#coupon-input")
        self.apply_coupon_button: Locator = page.locator("#apply-coupon-btn")
        self.coupon_msg: Locator = page.locator("#coupon-msg")

        self.subtotal_value: Locator = page.locator("#subtotal-val")
        self.discount_value: Locator = page.locator("#discount-val")
        self.total_value: Locator = page.locator("#total-val")
        self.proceed_checkout_button: Locator = page.locator("#proceed-checkout-btn")

    def close_cart(self):
        self.click(self.close_cart_button, "Close Cart Button")

    def remove_item(self, index: int = 0):
        remove_btn = self.page.locator("[data-test='remove-cart-item']").nth(index)
        self.click(remove_btn, f"Remove Item at index {index}")

    def apply_coupon(self, coupon_code: str):
        self.fill(self.coupon_input, coupon_code, "Coupon Code Input")
        self.click(self.apply_coupon_button, "Apply Coupon Button")

    def proceed_to_checkout(self):
        self.click(self.proceed_checkout_button, "Proceed to Checkout Button")

    def get_cart_item_count(self) -> int:
        return self.cart_rows.count()

    def get_subtotal(self) -> float:
        text = self.subtotal_value.inner_text()
        return float(text.replace("$", "").strip())

    def get_discount(self) -> float:
        text = self.discount_value.inner_text()
        return float(text.replace("$", "").strip())

    def get_total(self) -> float:
        text = self.total_value.inner_text()
        return float(text.replace("$", "").strip())
