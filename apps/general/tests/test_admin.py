import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.admin import (
CategoryAdmin,
CountryAdmin,
CurrencyAdmin,
EmailNotificationAdmin,
IndustryAdmin,
NotificationAdmin,
PeriodAdmin,
SectorAdmin,
TagAdmin,
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCategoryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCountryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCurrencyAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEmailNotificationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestIndustryAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNotificationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestPeriodAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSectorAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTagAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
