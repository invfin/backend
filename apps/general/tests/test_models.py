import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.models import (
Category,
Country,
Currency,
EmailNotification,
EscritosClassification,
Industry,
Notification,
Period,
Sector,
Tag,
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCategory(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCountry(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestCurrency(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestEmailNotification(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEscritosClassification(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestIndustry(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestNotification(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPeriod(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestSector(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestTag(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
