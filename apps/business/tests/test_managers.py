import vcr
from model_bakery import baker

from django.test import TestCase

from apps.business.managers import (
ProductManager,
)

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestProductManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
