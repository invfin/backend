import vcr
from model_bakery import baker

from django.test import TestCase

from apps.screener.admin import (
FavoritesEtfsHistorialAdmin,
FavoritesEtfsListAdmin,
FavoritesStocksHistorialAdmin,
FavoritesStocksListAdmin,
UserCompanyObservationAdmin,
UserScreenerMediumPredictionAdmin,
UserScreenerSimplePredictionAdmin,
YahooScreenerAdmin,
)

screener_vcr = vcr.VCR(
    cassette_library_dir='cassettes/screener/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestFavoritesEtfsHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFavoritesEtfsListAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFavoritesStocksHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFavoritesStocksListAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserCompanyObservationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserScreenerMediumPredictionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserScreenerSimplePredictionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestYahooScreenerAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
