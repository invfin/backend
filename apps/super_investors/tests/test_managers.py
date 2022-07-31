import vcr
from model_bakery import baker

from django.test import TestCase

from apps.super_investors.managers import (
SuperinvestorHistoryManager,
SuperinvestorManager,
)

super_investors_vcr = vcr.VCR(
    cassette_library_dir='cassettes/super_investors/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestSuperinvestorHistoryManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_company_in_current_portfolios(self):
        pass
    

class TestSuperinvestorManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_all_buys(self):
        pass
    
    def test_all_sells(self):
        pass
    
    def test_current_positions(self):
        pass
    
    def test_resume_current_positions(self):
        pass
    
