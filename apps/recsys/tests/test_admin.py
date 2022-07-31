import vcr
from model_bakery import baker

from django.test import TestCase

from apps.recsys.admin import (
BaseModelRecommendededAdmin,
UserCompanyRecommendedAdmin,
UserProductComplementaryRecommendedAdmin,
UserPromotionRecommendedAdmin,
UserPublicBlogRecommendedAdmin,
UserQuestionRecommendedAdmin,
UserTermRecommendedAdmin,
VisiteurCompanyRecommendedAdmin,
VisiteurProductComplementaryRecommendedAdmin,
VisiteurPromotionRecommendedAdmin,
VisiteurPublicBlogRecommendedAdmin,
VisiteurQuestionRecommendedAdmin,
VisiteurTermRecommendedAdmin,
)

recsys_vcr = vcr.VCR(
    cassette_library_dir='cassettes/recsys/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseModelRecommendededAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserCompanyRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserProductComplementaryRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserPromotionRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserPublicBlogRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserQuestionRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserTermRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurCompanyRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurProductComplementaryRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPromotionRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPublicBlogRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurQuestionRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurTermRecommendedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
