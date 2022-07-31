import vcr
from model_bakery import baker

from django.test import TestCase

from apps.empresas.models import (
BalanceSheet,
CashflowStatement,
Company,
CompanyGrowth,
CompanyStockPrice,
CompanyUpdateLog,
EficiencyRatio,
EnterpriseValueRatio,
Exchange,
ExchangeOrganisation,
FreeCashFlowRatio,
IncomeStatement,
InstitutionalOrganization,
LiquidityRatio,
MarginRatio,
NonGaap,
OperationRiskRatio,
PerShareValue,
PriceToRatio,
RentabilityRatio,
TopInstitutionalOwnership,
)

empresas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/empresas/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBalanceSheet(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCashflowStatement(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCompany(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_check_checkings(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_modify_checkings(self):
        pass
    

class TestCompanyGrowth(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCompanyStockPrice(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCompanyUpdateLog(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestEficiencyRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestEnterpriseValueRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestExchange(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestExchangeOrganisation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFreeCashFlowRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestIncomeStatement(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestInstitutionalOrganization(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestLiquidityRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestMarginRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestNonGaap(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestOperationRiskRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestPerShareValue(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestPriceToRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestRentabilityRatio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestTopInstitutionalOwnership(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
