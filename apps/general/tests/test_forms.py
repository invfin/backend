import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.forms import (
DefaultNewsletterForm,
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestDefaultNewsletterForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_annotate_changes(self):
        pass
    
    def test_creating_newsletter(self):
        pass
    
    def test_send_email(self):
        pass
    
