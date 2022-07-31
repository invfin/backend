import vcr
from model_bakery import baker

from django.test import TestCase

from apps.screener.forms import (
UserCompanyObservationForm,
)

screener_vcr = vcr.VCR(
    cassette_library_dir='cassettes/screener/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestUserCompanyObservationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
