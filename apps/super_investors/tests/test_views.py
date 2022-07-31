import vcr
from model_bakery import baker

from django.test import TestCase

from apps.super_investors.views import (
AllSuperinvestorsView,
SuperinvestorView,
)

super_investors_vcr = vcr.VCR(
    cassette_library_dir='cassettes/super_investors/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAllSuperinvestorsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_queryset(self):
        pass
    

class TestSuperinvestorView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_object(self):
        pass
    
