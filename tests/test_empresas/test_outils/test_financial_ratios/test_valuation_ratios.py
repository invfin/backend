from django.test import TestCase

from apps.empresas.models import IncomeStatement
from apps.empresas.outils.financial_ratios.valuation_ratios import ValuationRatios

from bfet import DjangoTestingModel
import pandas as pd

class TestValuationRatios(TestCase):
    def test_opa(self):
        inc = DjangoTestingModel.create(IncomeStatement)
        df = pd.DataFrame(IncomeStatement.objects.values())
        ndf = df.drop(columns=["id"])
        nic = IncomeStatement.objects.create(**ndf.to_dict('records')[0])

    def test_calculate_price_to_book(self):
        assert 1.88 == ValuationRatios.calculate_price_to_book(23.33, 12.42)

    def test_calculate_price_to_cash(self):
        assert 1.88 == ValuationRatios.calculate_price_to_cash(23.33, 12.42)

    def test_calculate_price_to_earnings(self):
        assert 1.88 == ValuationRatios.calculate_price_to_earnings(23.33, 12.42)

    def test_calculate_price_to_earnings_growth(self):
        assert 1.88 == ValuationRatios.calculate_price_to_earnings_growth(23.33, 12.42)

    def test_calculate_price_to_sales(self):
        assert 1.88 == ValuationRatios.calculate_price_to_sales(23.33, 12.42)

    def test_calculate_price_to_total_assets(self):
        assert 1.88 == ValuationRatios.calculate_price_to_total_assets(23.33, 12.42)

    def test_calculate_price_to_fcf(self):
        assert 1.88 == ValuationRatios.calculate_price_to_fcf(23.33, 12.42)

    def test_calculate_price_to_operating_cf(self):
        assert 1.88 == ValuationRatios.calculate_price_to_operating_cf(23.33, 12.42)

    def test_calculate_price_to_tangible_assets(self):
        assert 1.88 == ValuationRatios.calculate_price_to_tangible_assets(23.33, 12.42)

