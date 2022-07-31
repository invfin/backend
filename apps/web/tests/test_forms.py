import vcr
from model_bakery import baker

from django.test import TestCase

from apps.web.forms import (
ContactForm,
WebEmailForm,
)

web_vcr = vcr.VCR(
    cassette_library_dir='cassettes/web/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestContactForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_send_email(self):
        pass
    

class TestWebEmailForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_save(self):
        pass
    
