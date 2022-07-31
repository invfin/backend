import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.models import (
FavoritesTermsHistorial,
FavoritesTermsList,
Term,
TermContent,
TermCorrection,
TermsComment,
TermsRelatedToResume,
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestFavoritesTermsHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestFavoritesTermsList(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestTerm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_link(self):
        pass
    

class TestTermContent(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_link(self):
        pass
    

class TestTermCorrection(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_save(self):
        pass
    

class TestTermsComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_absolute_url(self):
        pass
    

class TestTermsRelatedToResume(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
