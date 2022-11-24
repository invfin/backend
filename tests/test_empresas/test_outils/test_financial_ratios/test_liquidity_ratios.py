from django.test import TestCase

from apps.empresas.outils.financial_ratios.liquidity_ratios import LiquidityRatios


class TestLiquidityRatios(TestCase):
    def test_calculate_cash_ratio(self):
        print(LiquidityRatios.calculate_cash_ratio())
        assert 0 == LiquidityRatios.calculate_cash_ratio()

    def test_calculate_current_ratio(self):
        print(LiquidityRatios.calculate_current_ratio())
        assert 0 == LiquidityRatios.calculate_current_ratio()

    def test_calculate_quick_ratio(self):
        print(LiquidityRatios.calculate_quick_ratio())
        assert 0 == LiquidityRatios.calculate_quick_ratio()

    def test_calculate_operating_cashflow_ratio(self):
        print(LiquidityRatios.calculate_operating_cashflow_ratio())
        assert 0 == LiquidityRatios.calculate_operating_cashflow_ratio()

    def test_calculate_debt_to_equity(self):
        print(LiquidityRatios.calculate_debt_to_equity())
        assert 0 == LiquidityRatios.calculate_debt_to_equity()
