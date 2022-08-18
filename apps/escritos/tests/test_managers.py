import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.managers import (
TermManager,
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestTermManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_clean_terms(self):
        pass
    
    def test_clean_terms_with_resume(self):
        pass
    
    def test_get_random(self):
        pass
    
    def test_random_clean(self):
        pass
    
