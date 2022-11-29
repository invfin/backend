from django.test import TestCase

from apps.empresas.outils.financial_ratios.efficiency_ratios import EfficiencyRatios


class TestEfficiencyRatios(TestCase):
    def test_calculate_days_inventory_outstanding(self):
        assert 0 == EfficiencyRatios.calculate_days_inventory_outstanding(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_days_inventory_outstanding(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_days_inventory_outstanding(234.67, 0)

    def test_calculate_days_payables_outstanding(self):
        assert 0 == EfficiencyRatios.calculate_days_payables_outstanding(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_days_payables_outstanding(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_days_payables_outstanding(234.67, 0)

    def test_calculate_days_sales_outstanding(self):
        assert 0 == EfficiencyRatios.calculate_days_sales_outstanding(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_days_sales_outstanding(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_days_sales_outstanding(234.67, 0)

    def test_calculate_operating_cycle(self):
        assert 0 == EfficiencyRatios.calculate_operating_cycle(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_operating_cycle(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_operating_cycle(234.67, 0)

    def test_calculate_cash_conversion_cycle(self):
        assert 0 == EfficiencyRatios.calculate_cash_conversion_cycle(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_cash_conversion_cycle(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_cash_conversion_cycle(234.67, 0)

    def test_calculate_asset_turnover(self):
        assert 0 == EfficiencyRatios.calculate_asset_turnover(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_asset_turnover(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_asset_turnover(234.67, 0)

    def test_calculate_inventory_turnover(self):
        assert 0 == EfficiencyRatios.calculate_inventory_turnover(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_inventory_turnover(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_inventory_turnover(234.67, 0)

    def test_calculate_fixed_asset_turnover(self):
        assert 0 == EfficiencyRatios.calculate_fixed_asset_turnover(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_fixed_asset_turnover(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_fixed_asset_turnover(234.67, 0)

    def test_calculate_payables_turnover(self):
        assert 0 == EfficiencyRatios.calculate_payables_turnover(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_payables_turnover(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_payables_turnover(234.67, 0)

    def test_calculate_fcf_to_operating_cf(self):
        assert 0 == EfficiencyRatios.calculate_fcf_to_operating_cf(234.67, 3333)
        assert 0 == EfficiencyRatios.calculate_fcf_to_operating_cf(234.67, 3.98)
        assert 0 == EfficiencyRatios.calculate_fcf_to_operating_cf(234.67, 0)

