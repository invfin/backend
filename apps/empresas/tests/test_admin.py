import vcr
from model_bakery import baker

from django.test import TestCase

from apps.empresas.admin import (
BalanceSheetAdmin,
CashflowStatementAdmin,
CompanyAdmin,
CompanyGrowthAdmin,
CompanyStockPriceAdmin,
CompanyUpdateLogAdmin,
EficiencyRatioAdmin,
EnterpriseValueRatioAdmin,
ExchangeAdmin,
ExchangeOrganisationAdmin,
FreeCashFlowRatioAdmin,
IncomeStatementAdmin,
InstitutionalOrganizationAdmin,
LiquidityRatioAdmin,
MarginRatioAdmin,
NonGaapAdmin,
OperationRiskRatioAdmin,
PerShareValueAdmin,
PriceToRatioAdmin,
RentabilityRatioAdmin,
TopInstitutionalOwnershipAdmin,
)

empresas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/empresas/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBalanceSheetAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCashflowStatementAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyGrowthAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyStockPriceAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyUpdateLogAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEficiencyRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEnterpriseValueRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestExchangeAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestExchangeOrganisationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestFreeCashFlowRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestIncomeStatementAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestInstitutionalOrganizationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestLiquidityRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestMarginRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNonGaapAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestOperationRiskRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPerShareValueAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPriceToRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRentabilityRatioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTopInstitutionalOwnershipAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
