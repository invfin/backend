import vcr
from model_bakery import baker

from django.test import TestCase

from apps.socialmedias.admin import (
BlogSharedHistorialAdmin,
CompanySharedHistorialAdmin,
DefaultContentAdmin,
DefaultTilteAdmin,
EmojiAdmin,
HashtagAdmin,
NewsSharedHistorialAdmin,
ProfileSharedHistorialAdmin,
QuestionSharedHistorialAdmin,
TermSharedHistorialAdmin,
)

socialmedias_vcr = vcr.VCR(
    cassette_library_dir='cassettes/socialmedias/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBlogSharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanySharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestDefaultContentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestDefaultTilteAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestEmojiAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestHashtagAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestNewsSharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProfileSharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestQuestionSharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermSharedHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
