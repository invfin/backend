from django.test import TestCase

from bfet import DjangoTestingModel

from src.empresas.models import Company


class TestBaseStatementManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.company = DjangoTestingModel.create(Company)

    def test_average_margins(self):
        self.company.inc_statements.all().average_margins()
        assert 1111 == 2222

    def test_average_efficiency_ratios(self):
        assert 1111 == 2222

    def test_average_growth_rates(self):
        assert 1111 == 2222

    def test_average_per_share_values(self):
        assert 1111 == 2222

    def test_average_price_to_ratios(self):
        assert 1111 == 2222

    def test_average_liquidity_ratios(self):
        assert 1111 == 2222

    def test_average_rentability_ratios(self):
        assert 1111 == 2222

    def test_average_operation_risks_ratios(self):
        assert 1111 == 2222

    def test_average_ev_ratios(self):
        assert 1111 == 2222

