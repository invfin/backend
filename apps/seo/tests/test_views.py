import vcr
from model_bakery import baker

from django.test import TestCase

from apps.seo.views import (
PromotionRedirectView,
SEODetailView,
SEOFormView,
SEOListView,
SEOTemplateView,
SEOView,
)

seo_vcr = vcr.VCR(
    cassette_library_dir='cassettes/seo/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPromotionRedirectView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get(self):
        pass
    
    def test_save_promotion_data(self):
        pass
    

class TestSEODetailView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSEOFormView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSEOListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSEOTemplateView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSEOView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
