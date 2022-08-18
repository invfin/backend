import vcr
from model_bakery import baker

from django.test import TestCase

from apps.cartera.models import (
Asset,
CashflowMovement,
CashflowMovementCategory,
FinancialObjectif,
Income,
Patrimonio,
PositionMovement,
Spend,
)

cartera_vcr = vcr.VCR(
    cassette_library_dir='cassettes/cartera/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAsset(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCashflowMovement(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCashflowMovementCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFinancialObjectif(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestIncome(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPatrimonio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_ahorros_totales(self):
        pass
    
    def test_cantidad_total_invertida(self):
        pass
    
    def test_gastos_totales(self):
        pass
    
    def test_positions_segmentation_information(self):
        pass
    
    def test_prepare_chart_data(self):
        pass
    

class TestPositionMovement(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestSpend(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
