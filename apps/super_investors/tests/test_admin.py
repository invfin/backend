import vcr
from model_bakery import baker

from django.test import TestCase

from apps.super_investors.admin import (
SuperinvestorActivityAdmin,
SuperinvestorAdmin,
SuperinvestorHistoryAdmin,
)

super_investors_vcr = vcr.VCR(
    cassette_library_dir='cassettes/super_investors/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestSuperinvestorActivityAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSuperinvestorAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSuperinvestorHistoryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
