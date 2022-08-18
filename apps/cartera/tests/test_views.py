import vcr
from model_bakery import baker

from django.test import TestCase

from apps.cartera.views import (
DefaultCateraView,
InicioCarteraView,
InicioCashflowView,
InicioPortfolioView,
)

cartera_vcr = vcr.VCR(
    cassette_library_dir='cassettes/cartera/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestDefaultCateraView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestInicioCarteraView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestInicioCashflowView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestInicioPortfolioView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
