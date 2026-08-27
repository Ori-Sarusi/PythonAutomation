import random
import pytest
from playwright.sync_api import expect
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from pages.cart_page import CartPage
from config import config

class TestCart:
    """
    Generic & Dynamic Cart Test Suite:
    - No hardcoded IDs or static product prices.
    - Dynamically queries available items, picks randomly, and asserts calculated totals.
    - Full coverage: Positive (single, multiple, repeats), Negative (coupons, empty cart), Edge Cases.
    """

    @pytest.fixture(autouse=True)
    def setup_logged_in_user(self, auth_page: AuthPage):
        """Precondition: start each test logged in on the catalog page."""
        auth_page.navigate(config.BASE_URL)
        auth_page.login(config.STANDARD_USER, config.PASSWORD)

    # -------------------------------------------------------------
    # 1. GENERIC POSITIVE TESTS (Dynamic Selection & Math Validation)
    # -------------------------------------------------------------
    def test_add_random_single_item_to_cart(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Randomly picks 1 available product, reads its live UI price, adds it, and asserts cart match."""
        total_products = catalog_page.get_products_count()
        assert total_products > 0, "No products found in catalog grid!"

        # Pick random index from available products
        random_index = random.randint(0, total_products - 1)
        selected_product = catalog_page.add_product_to_cart_by_index(random_index)

        expect(catalog_page.cart_count_badge).to_have_text("1")

        catalog_page.open_cart()
        expect(cart_page.cart_section).to_be_visible()
        assert cart_page.get_cart_item_count() == 1
        assert cart_page.get_subtotal() == selected_product["price"]
        assert cart_page.get_total() == selected_product["price"]

    @pytest.mark.parametrize("item_count", [2, 3, 5])
    def test_add_multiple_random_items_and_calculate_sum(
        self, catalog_page: CatalogPage, cart_page: CartPage, item_count: int
    ):
        """Randomly selects N products, accumulates their dynamic prices, and validates exact subtotal."""
        total_products = catalog_page.get_products_count()
        assert total_products > 0

        # Sample up to available catalog size
        sample_size = min(item_count, total_products)
        random_indices = random.sample(range(total_products), sample_size)

        expected_subtotal = 0.0
        for idx in random_indices:
            added_item = catalog_page.add_product_to_cart_by_index(idx)
            expected_subtotal += added_item["price"]

        expect(catalog_page.cart_count_badge).to_have_text(str(sample_size))

        catalog_page.open_cart()
        assert cart_page.get_cart_item_count() == sample_size
        assert round(cart_page.get_subtotal(), 2) == round(expected_subtotal, 2)
        assert round(cart_page.get_total(), 2) == round(expected_subtotal, 2)

    def test_add_duplicate_random_item_multiple_times(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Picks a random item, adds it 3 times, and verifies multiplier calculation."""
        total_products = catalog_page.get_products_count()
        random_index = random.randint(0, total_products - 1)

        product_details = catalog_page.get_product_details_by_index(random_index)
        for _ in range(3):
            catalog_page.add_product_to_cart_by_index(random_index)

        expect(catalog_page.cart_count_badge).to_have_text("3")

        catalog_page.open_cart()
        assert cart_page.get_cart_item_count() == 3
        expected_total = round(product_details["price"] * 3, 2)
        assert round(cart_page.get_subtotal(), 2) == expected_total
        assert round(cart_page.get_total(), 2) == expected_total

    def test_remove_random_item_from_cart(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Adds 2 random items, removes the first one, and verifies cart recalculated accurately."""
        total_products = catalog_page.get_products_count()
        indices = random.sample(range(total_products), 2)

        item1 = catalog_page.add_product_to_cart_by_index(indices[0])
        item2 = catalog_page.add_product_to_cart_by_index(indices[1])

        catalog_page.open_cart()
        assert cart_page.get_cart_item_count() == 2

        # Remove item 1
        cart_page.remove_item(index=0)
        assert cart_page.get_cart_item_count() == 1
        assert round(cart_page.get_subtotal(), 2) == round(item2["price"], 2)
        expect(catalog_page.cart_count_badge).to_have_text("1")

    def test_valid_promo_coupon_calculation(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Adds random items and validates that 10% coupon is calculated on true total subtotal."""
        total_products = catalog_page.get_products_count()
        indices = random.sample(range(total_products), min(2, total_products))

        for idx in indices:
            catalog_page.add_product_to_cart_by_index(idx)

        catalog_page.open_cart()
        cart_page.apply_coupon("SAVE10")

        expect(cart_page.coupon_msg).to_be_visible()
        expect(cart_page.coupon_msg).to_contain_text("applied")

        subtotal = cart_page.get_subtotal()
        expected_discount = round(subtotal * 0.10, 2)
        expected_total = round(subtotal - expected_discount, 2)

        assert round(cart_page.get_discount(), 2) == expected_discount, (
            f"Expected discount {expected_discount}, but got {cart_page.get_discount()}"
        )
        assert round(cart_page.get_total(), 2) == expected_total

    # -------------------------------------------------------------
    # 2. NEGATIVE TESTS (Invalid Coupons, Empty Inputs, Empty Cart)
    # -------------------------------------------------------------
    @pytest.mark.parametrize("invalid_code", [
        "INVALID10",
        "DISCOUNT99",
        "12345",
        "save_ten"
    ])
    def test_invalid_coupon_codes(self, catalog_page: CatalogPage, cart_page: CartPage, invalid_code: str):
        """Invalid coupons must be rejected with an error message and zero discount."""
        total_products = catalog_page.get_products_count()
        catalog_page.add_product_to_cart_by_index(random.randint(0, total_products - 1))

        catalog_page.open_cart()
        cart_page.apply_coupon(invalid_code)

        expect(cart_page.coupon_msg).to_be_visible()
        expect(cart_page.coupon_msg).to_have_text("Invalid coupon code.")
        assert cart_page.get_discount() == 0.00
        assert cart_page.get_total() == cart_page.get_subtotal()

    def test_empty_coupon_code_submission(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Submitting blank spaces or empty string in promo field should be rejected."""
        total_products = catalog_page.get_products_count()
        catalog_page.add_product_to_cart_by_index(random.randint(0, total_products - 1))

        catalog_page.open_cart()
        cart_page.apply_coupon("   ")

        expect(cart_page.coupon_msg).to_be_visible()
        expect(cart_page.coupon_msg).to_have_text("Invalid coupon code.")
        assert cart_page.get_discount() == 0.00

    def test_open_empty_cart_view(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Opening cart with 0 items displays empty placeholder and $0.00 totals."""
        catalog_page.open_cart()

        expect(cart_page.cart_items_container).to_contain_text("Your cart is empty")
        assert cart_page.get_subtotal() == 0.00
        assert cart_page.get_total() == 0.00

    # -------------------------------------------------------------
    # 3. EDGE CASES (Boundary Conditions & User Flow Variations)
    # -------------------------------------------------------------
    def test_coupon_case_insensitivity(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Lowercase promo code 'save10' should be accepted just like 'SAVE10'."""
        total_products = catalog_page.get_products_count()
        catalog_page.add_product_to_cart_by_index(random.randint(0, total_products - 1))

        catalog_page.open_cart()
        cart_page.apply_coupon("save10")

        expect(cart_page.coupon_msg).to_be_visible()
        expect(cart_page.coupon_msg).to_contain_text("applied")
        assert cart_page.get_discount() > 0

    def test_remove_all_items_until_empty(self, catalog_page: CatalogPage, cart_page: CartPage):
        """Add multiple random items, delete all sequentially, assert state returns to empty."""
        total_products = catalog_page.get_products_count()
        indices = random.sample(range(total_products), min(2, total_products))

        for idx in indices:
            catalog_page.add_product_to_cart_by_index(idx)

        catalog_page.open_cart()
        for _ in range(len(indices)):
            cart_page.remove_item(0)

        expect(cart_page.cart_items_container).to_contain_text("Your cart is empty")
        expect(catalog_page.cart_count_badge).to_have_text("0")
        assert cart_page.get_subtotal() == 0.00
        assert cart_page.get_total() == 0.00
