import vcr
from model_bakery import baker

from django.test import TestCase

from apps.api.admin import (
BaseRequestAPIAdmin,
CompanyRequestAPIAdmin,
EndpointAdmin,
EndpointsCategoryAdmin,
KeyAdmin,
ReasonKeyRequestedAdmin,
SuperinvestorRequestAPIAdmin,
TermRequestAPIAdmin,
)

api_vcr = vcr.VCR(
    cassette_library_dir='cassettes/api/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseRequestAPIAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanyRequestAPIAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEndpointAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEndpointsCategoryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestKeyAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_user_link(self):
        pass
    

class TestReasonKeyRequestedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSuperinvestorRequestAPIAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermRequestAPIAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
