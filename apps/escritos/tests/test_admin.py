import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.admin import (
TermAdmin,
TermContentAdmin,
TermContentInline,
TermCorrectionAdmin,
TermsCommentAdmin,
TermsRelatedToResumeAdmin,
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestTermAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermContentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermContentInline(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermCorrectionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermsCommentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermsRelatedToResumeAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
