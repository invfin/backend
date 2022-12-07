from django.test import TestCase

from apps.empresas.outils.financial_ratios.rentability_ratios import RentabilityRatios


class TestRentabilityRatios(TestCase):
    def test_calculate_roa(self):
        assert 55.0 == RentabilityRatios.calculate_roa(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_roa(5.9, 4, False)

    def test_calculate_roc(self):
        assert 55.0 == RentabilityRatios.calculate_roc(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_roc(5.9, 4, False)

    def test_calculate_roce(self):
        assert 55.0 == RentabilityRatios.calculate_roce(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_roce(5.9, 4, False)

    def test_calculate_rota(self):
        assert 55.0 == RentabilityRatios.calculate_rota(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_rota(5.9, 4, False)

    def test_calculate_roic(self):
        assert 30.0 == RentabilityRatios.calculate_roic(23.89, 11, 43.6)
        assert 1.45 == RentabilityRatios.calculate_roic(5.9, 0.09, 4, False)

    def test_calculate_nopat_roic(self):
        assert 55.0 == RentabilityRatios.calculate_nopat_roic(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_nopat_roic(5.9, 4, False)

    def test_calculate_rogic(self):
        assert 55.0 == RentabilityRatios.calculate_rogic(23.89, 43.6)
        assert 1.48 == RentabilityRatios.calculate_rogic(5.9, 4, False)
