import vcr
from model_bakery import baker

from django.test import TestCase

from apps.screener.views import (
AllYahooScreenersView,
BuyCompanyInfo,
CompanyDetailsView,
CompanyLookUpView,
CompanyScreenerInicioView,
EtfDetailsView,
EtfScreenerInicioView,
ScreenerInicioView,
YahooScreenerView,
)

screener_vcr = vcr.VCR(
    cassette_library_dir='cassettes/screener/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAllYahooScreenersView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestBuyCompanyInfo(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    

class TestCompanyDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_object(self):
        pass
    
    def test_save_company_in_session(self):
        pass
    

class TestCompanyLookUpView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    

class TestCompanyScreenerInicioView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_queryset(self):
        pass
    

class TestEtfDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_object(self):
        pass
    

class TestEtfScreenerInicioView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestScreenerInicioView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestYahooScreenerView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
