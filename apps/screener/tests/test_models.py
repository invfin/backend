import vcr
from model_bakery import baker

from django.test import TestCase

from apps.screener.models import (
BasePrediction,
CompanyInformationBought,
FavoritesEtfsHistorial,
FavoritesEtfsList,
FavoritesStocksHistorial,
FavoritesStocksList,
UserCompanyObservation,
UserScreenerMediumPrediction,
UserScreenerSimplePrediction,
YahooScreener,
)

screener_vcr = vcr.VCR(
    cassette_library_dir='cassettes/screener/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBasePrediction(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyInformationBought(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFavoritesEtfsHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFavoritesEtfsList(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFavoritesStocksHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFavoritesStocksList(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestUserCompanyObservation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    

class TestUserScreenerMediumPrediction(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestUserScreenerSimplePrediction(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestYahooScreener(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_save(self):
        pass
    
