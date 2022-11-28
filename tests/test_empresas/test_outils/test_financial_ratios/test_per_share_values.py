from django.test import TestCase

from apps.empresas.outils.financial_ratios.per_share_values import PerShareValues


class TestPerShareValues(TestCase):
    def test_calculate_sales_ps(self):
        assert 0.0033 == PerShareValues.calculate_sales_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_sales_ps(324534534, 98238192546)

    def test_calculate_book_ps(self):
        assert 0.0033 == PerShareValues.calculate_book_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_book_ps(324534534, 98238192546)

    def test_calculate_tangible_ps(self):
        assert 0.0033 == PerShareValues.calculate_tangible_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_tangible_ps(324534534, 98238192546)

    def test_calculate_fcf_ps(self):
        assert 0.0033 == PerShareValues.calculate_fcf_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_fcf_ps(324534534, 98238192546)

    def test_calculate_eps(self):
        assert 0.0033 == PerShareValues.calculate_eps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_eps(324534534, 98238192546)

    def test_calculate_cash_ps(self):
        assert 0.0033 == PerShareValues.calculate_cash_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_cash_ps(324534534, 98238192546)

    def test_calculate_operating_cf_ps(self):
        assert 0.0033 == PerShareValues.calculate_operating_cf_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_operating_cf_ps(324534534, 98238192546)

    def test_calculate_capex_ps(self):
        assert 0.0033 == PerShareValues.calculate_capex_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_capex_ps(324534534, 98238192546)

    def test_calculate_total_assets_ps(self):
        assert 0.0033 == PerShareValues.calculate_total_assets_ps(324534534.34, 98238192546)
        assert 0.0033 == PerShareValues.calculate_total_assets_ps(324534534, 98238192546)
