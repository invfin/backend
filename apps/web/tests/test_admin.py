import vcr
from model_bakery import baker

from django.test import TestCase

from apps.web.admin import (
PromotionAdmin,
PromotionCampaignAdmin,
WebsiteEmailAdmin,
WebsiteEmailTrackAdmin,
WebsiteEmailsTypeAdmin,
WebsiteLegalPageAdmin,
)

web_vcr = vcr.VCR(
    cassette_library_dir='cassettes/web/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPromotionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPromotionCampaignAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWebsiteEmailAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWebsiteEmailTrackAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWebsiteEmailsTypeAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestWebsiteLegalPageAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
