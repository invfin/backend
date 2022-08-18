import vcr
from model_bakery import baker

from django.test import TestCase

from apps.recsys.models import (
BaseModelRecommended,
BaseUserModelRecommended,
BaseVisiteurModelRecommended,
UserCompanyRecommended,
UserProductComplementaryRecommended,
UserPromotionRecommended,
UserPublicBlogRecommended,
UserQuestionRecommended,
UserTermRecommended,
VisiteurCompanyRecommended,
VisiteurProductComplementaryRecommended,
VisiteurPromotionRecommended,
VisiteurPublicBlogRecommended,
VisiteurQuestionRecommended,
VisiteurTermRecommended,
)

recsys_vcr = vcr.VCR(
    cassette_library_dir='cassettes/recsys/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseModelRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_full_clean(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_save(self):
        pass
    

class TestBaseUserModelRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestBaseVisiteurModelRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestUserCompanyRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserProductComplementaryRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserPromotionRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserPublicBlogRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserQuestionRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserTermRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurCompanyRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurProductComplementaryRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPromotionRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPublicBlogRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurQuestionRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurTermRecommended(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
