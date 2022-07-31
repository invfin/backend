import vcr
from model_bakery import baker

from django.test import TestCase

from apps.empresas.views import (
ExcelAPIBalance,
ExcelAPICashflow,
ExcelAPIIncome,
)

empresas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/empresas/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestExcelAPIBalance(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestExcelAPICashflow(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestExcelAPIIncome(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
