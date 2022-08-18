import vcr
from model_bakery import baker

from django.test import TestCase

from apps.api.managers import (
KeyManager,
)

api_vcr = vcr.VCR(
    cassette_library_dir='cassettes/api/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestKeyManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_create_unique_key(self):
        pass
    
    def test_cuota_remainig(self):
        pass
    
    def test_generate_key(self):
        pass
    
    def test_get_key(self):
        pass
    
    def test_has_cuota(self):
        pass
    
    def test_key_for_docs(self):
        pass
    
    def test_key_is_active(self):
        pass
    
    def test_return_if_key(self):
        pass
    
