import vcr
from model_bakery import baker

from django.test import TestCase

from apps.socialmedias.managers import (
DefaultContentManager,
EmojisManager,
HashtagsManager,
TitlesManager,
)

socialmedias_vcr = vcr.VCR(
    cassette_library_dir='cassettes/socialmedias/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestDefaultContentManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_random_content(self):
        pass
    

class TestEmojisManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_random_emojis(self):
        pass
    

class TestHashtagsManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_random_hashtags(self):
        pass
    

class TestTitlesManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_random_title(self):
        pass
    
