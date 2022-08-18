import vcr
from model_bakery import baker

from django.test import TestCase

from apps.cartera.admin import (
AssetAdmin,
FinancialObjectifAdmin,
IncomeAdmin,
PatrimonioAdmin,
PositionMovementAdmin,
SpendAdmin,
)

cartera_vcr = vcr.VCR(
    cassette_library_dir='cassettes/cartera/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAssetAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFinancialObjectifAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestIncomeAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPatrimonioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPositionMovementAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSpendAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
