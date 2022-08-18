import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.views import (
GlosarioView,
TermCorrectionView,
TermDetailsView,
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestGlosarioView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_queryset(self):
        pass
    

class TestTermCorrectionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form_valid(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_object(self):
        pass
    
    def test_post(self):
        pass
    

class TestTermDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
