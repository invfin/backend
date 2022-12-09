from src.empresas.outils.financial_ratios import CalculateFinancialRatios


class TestCalculateFinancialRatios:
    def test_calculate_efficiency_ratios(self):
        expected_data = {
            "days_inventory_outstanding": days_inventory_outstanding,
            "days_payables_outstanding": days_payables_outstanding,
            "days_sales_outstanding": days_sales_outstanding,
            "operating_cycle": operating_cycle,
            "cash_conversion_cycle": cash_conversion_cycle,
            "asset_turnover": asset_turnover,
            "inventory_turnover": inventory_turnover,
            "fixed_asset_turnover": fixed_asset_turnover,
            "payables_turnover": payables_turnover,
            "fcf_to_operating_cf": fcf_to_operating_cf,
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
        assert expected_data == CalculateFinancialRatios.calculate_efficiency_ratios(data)
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
