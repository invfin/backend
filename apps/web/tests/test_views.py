import vcr
from model_bakery import baker

from django.test import TestCase

from apps.web.views import (
CreateWebEmailView,
ExcelRedirectView,
HomePage,
LegalPages,
)

web_vcr = vcr.VCR(
    cassette_library_dir='cassettes/web/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCreateWebEmailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_success_url(self):
        pass
    
    def test_test_func(self):
        pass
    

class TestExcelRedirectView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_redirect_url(self):
        pass
    

class TestHomePage(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_render_to_response(self):
        pass
    

class TestLegalPages(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
