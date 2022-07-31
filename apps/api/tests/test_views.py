import vcr
from model_bakery import baker

from django.test import TestCase

from apps.api.views import (
APIDocumentation,
BaseAPIView,
ObtainAuthKey,
)

api_vcr = vcr.VCR(
    cassette_library_dir='cassettes/api/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAPIDocumentation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestBaseAPIView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_check_limitation(self):
        pass
    
    def test_final_responses(self):
        pass
    
    def test_find_query_value(self):
        pass
    
    def test_get(self):
        pass
    
    def test_get_object(self):
        pass
    
    def test_save_request(self):
        pass
    

class TestObtainAuthKey(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    
    def test_get_serializer(self):
        pass
    
    def test_get_serializer_context(self):
        pass
    
    def test_post(self):
        pass
    
