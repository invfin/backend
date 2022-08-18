import vcr
from model_bakery import baker

from django.test import TestCase

from apps.cartera.forms import (
AddCategoriesForm,
AddNewAssetForm,
BaseAssetMoveForm,
BaseForm,
CashflowMoveForm,
DefaultCurrencyForm,
FinancialObjectifForm,
PositionMovementForm,
)

cartera_vcr = vcr.VCR(
    cassette_library_dir='cassettes/cartera/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAddCategoriesForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    

class TestAddNewAssetForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    

class TestBaseAssetMoveForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_clean_date(self):
        pass
    

class TestBaseForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCashflowMoveForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    

class TestDefaultCurrencyForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    

class TestFinancialObjectifForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    

class TestPositionMovementForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___init__(self):
        pass
    
    def test_save(self):
        pass
    
