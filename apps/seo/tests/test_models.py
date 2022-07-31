import vcr
from model_bakery import baker

from django.test import TestCase

from apps.seo.models import (
BaseModelVisited,
BaseUserModelVisited,
BaseVisiteurModelVisited,
Journey,
MetaParameters,
MetaParametersHistorial,
UserCompanyVisited,
UserJourney,
UserPublicBlogVisited,
UserQuestionVisited,
UserTermVisited,
Visiteur,
VisiteurCompanyVisited,
VisiteurJourney,
VisiteurPublicBlogVisited,
VisiteurQuestionVisited,
VisiteurTermVisited,
VisiteurUserRelation,
)

seo_vcr = vcr.VCR(
    cassette_library_dir='cassettes/seo/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseModelVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestBaseUserModelVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestBaseVisiteurModelVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestJourney(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestMetaParameters(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestMetaParametersHistorial(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestUserCompanyVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserJourney(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserPublicBlogVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserQuestionVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserTermVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteur(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestVisiteurCompanyVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurJourney(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPublicBlogVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurQuestionVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurTermVisited(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurUserRelation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
