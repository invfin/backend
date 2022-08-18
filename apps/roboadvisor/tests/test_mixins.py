import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.mixins import (
ServicePaymentMixin,
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/mixins/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestServicePaymentMixin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_service_activity(self):
        pass
    
    def test_manage_service_activity(self):
        pass
    
    def test_return_results(self):
        pass
    
    def test_service_payment(self):
        pass
    
