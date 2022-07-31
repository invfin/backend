import vcr
from model_bakery import baker

from django.test import TestCase

from apps.socialmedias.models import (
BaseContentShared,
BlogSharedHistorial,
CompanySharedHistorial,
DefaultContent,
DefaultTilte,
Emoji,
Hashtag,
NewsSharedHistorial,
ProfileSharedHistorial,
QuestionSharedHistorial,
TermSharedHistorial,
)

socialmedias_vcr = vcr.VCR(
    cassette_library_dir='cassettes/socialmedias/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseContentShared(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestBlogSharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestCompanySharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestDefaultContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestDefaultTilte(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestEmoji(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestHashtag(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestNewsSharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestProfileSharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestQuestionSharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTermSharedHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
