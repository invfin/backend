from django.test import TestCase

from apps.empresas.outils.financial_ratios.liquidity_ratios import LiquidityRatios


class TestLiquidityRatios(TestCase):
    def test_calculate_cash_ratio(self):
        assert 0.54 == LiquidityRatios.calculate_cash_ratio(23.22, 43.11)
        assert 0 == LiquidityRatios.calculate_cash_ratio(23.33, 0)
        assert 0.54 == LiquidityRatios.calculate_cash_ratio(23.22, 43)

    def test_calculate_current_ratio(self):
        assert 0.54 == LiquidityRatios.calculate_current_ratio(23.22, 43.11)
        assert 0 == LiquidityRatios.calculate_current_ratio(23.33, 0)
        assert 0.54 == LiquidityRatios.calculate_current_ratio(23.22, 43)

    def test_calculate_quick_ratio(self):
        assert 1.77 == LiquidityRatios.calculate_quick_ratio(23.22, 53.278, 43.11)
        assert 0 == LiquidityRatios.calculate_quick_ratio(23.33, 53.278, 0)
        assert 1.78 == LiquidityRatios.calculate_quick_ratio(23.22, 53.278, 43)

    def test_calculate_operating_cashflow_ratio(self):
        assert 0.54 == LiquidityRatios.calculate_operating_cashflow_ratio(23.22, 43.11)
        assert 0 == LiquidityRatios.calculate_operating_cashflow_ratio(23.33, 0)
        assert 0.54 == LiquidityRatios.calculate_operating_cashflow_ratio(23.22, 43)

    def test_calculate_debt_to_equity(self):
        assert 0.54 == LiquidityRatios.calculate_debt_to_equity(23.22, 43.11)
        assert 0 == LiquidityRatios.calculate_debt_to_equity(23.33, 0)
        assert 0.54 == LiquidityRatios.calculate_debt_to_equity(23.22, 43)
