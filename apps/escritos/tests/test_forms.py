import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.forms import (
CreateCorrectionForm,
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCreateCorrectionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
