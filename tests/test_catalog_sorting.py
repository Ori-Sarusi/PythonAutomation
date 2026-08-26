import pytest
from pages.auth_page import AuthPage
from pages.catalog_page import CatalogPage
from config import config

class TestCatalogSorting:
    """
    Test suite for product catalog sorting options:
    - Name: A to Z
    - Price: Low to High
    - Price: High to Low
    """

    @pytest.fixture(autouse=True)
    def setup_logged_in_catalog(self, auth_page: AuthPage):
        """Precondition for every test: navigate and log in to reach the catalog."""
        auth_page.navigate(config.BASE_URL)
        auth_page.login(config.STANDARD_USER, config.PASSWORD)

    def test_sort_by_name_a_to_z(self, catalog_page: CatalogPage):
        catalog_page.sort_by("name-asc")
        actual_titles = catalog_page.get_all_product_titles()

        expected_titles = sorted(actual_titles)
        assert actual_titles == expected_titles, f"Products not sorted A-Z! Got: {actual_titles}"

    def test_sort_by_price_low_to_high(self, catalog_page: CatalogPage):
        catalog_page.sort_by("price-asc")
        actual_prices = catalog_page.get_all_product_prices()

        expected_prices = sorted(actual_prices)
        assert actual_prices == expected_prices, f"Prices not sorted Low to High! Got: {actual_prices}"

    def test_sort_by_price_high_to_low(self, catalog_page: CatalogPage):
        catalog_page.sort_by("price-desc")
        actual_prices = catalog_page.get_all_product_prices()

        expected_prices = sorted(actual_prices, reverse=True)
        assert actual_prices == expected_prices, f"Prices not sorted High to Low! Got: {actual_prices}"
