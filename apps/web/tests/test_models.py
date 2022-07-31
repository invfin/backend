import vcr
from model_bakery import baker

from django.test import TestCase

from apps.web.models import (
Promotion,
PromotionCampaign,
WebsiteEmail,
WebsiteEmailTrack,
WebsiteEmailsType,
WebsiteLegalPage,
)

web_vcr = vcr.VCR(
    cassette_library_dir='cassettes/web/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPromotion(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestPromotionCampaign(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestWebsiteEmail(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestWebsiteEmailTrack(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestWebsiteEmailsType(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestWebsiteLegalPage(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    
