from django.test import TestCase

from apps.empresas.outils.financial_ratios import CalculateFinancialRatios


class TestCalculateFinancialRatios(TestCase):
    def test_calculate_price_to_ratios(self):
        expected_data = {
            "price_book": 1.0,
            "price_cf": 5.0,
            "price_earnings": 4.72,
            "price_earnings_growth": 18.88,
            "price_sales": 2.94,
            "price_total_assets": 3.33,
            "price_fcf": 1.45,
            "price_operating_cf": 0,
            "price_tangible_assets": 0.83,
        }
        data = {
            "book_ps": 10,
            "cash_ps": 2,
            "current_price": 10,
            "eps": 2.12,
            "net_income_growth": 0.25,
            "sales_ps": 3.4,
            "total_assets_ps": 3,
            "fcf_ps": 6.92,
            "operating_cf_ps": 0,
            "tangible_ps": 12.12,
        }
        assert expected_data == CalculateFinancialRatios.calculate_price_to_ratios(data)

    def test_calculate_average_inventory(self):
        data = {
            "last_year_inventory": 16.22,
            "inventory": 12.22,
        }
        assert 14.22 == CalculateFinancialRatios.calculate_average_inventory(data)
