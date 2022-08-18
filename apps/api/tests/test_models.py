import vcr
from model_bakery import baker

from django.test import TestCase

from apps.api.models import (
BaseRequestAPI,
CompanyRequestAPI,
Endpoint,
EndpointsCategory,
Key,
ReasonKeyRequested,
SuperinvestorRequestAPI,
TermRequestAPI,
)

api_vcr = vcr.VCR(
    cassette_library_dir='cassettes/api/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseRequestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCompanyRequestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEndpoint(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestEndpointsCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestKey(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestReasonKeyRequested(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestSuperinvestorRequestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermRequestAPI(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
