import vcr
from model_bakery import baker

from django.test import TestCase

from apps.seo.admin import (
BaseModelVisitedAdmin,
MetaParametersAdmin,
MetaParametersHistorialAdmin,
SessionAdmin,
UserCompanyVisitedAdmin,
UserJourneyAdmin,
UserPublicBlogVisitedAdmin,
UserQuestionVisitedAdmin,
UserTermVisitedAdmin,
VisiteurAdmin,
VisiteurCompanyVisitedAdmin,
VisiteurJourneyAdmin,
VisiteurJourneyResource,
VisiteurPublicBlogVisitedAdmin,
VisiteurQuestionVisitedAdmin,
VisiteurTermVisitedAdmin,
VisiteurUserRelationAdmin,
)

seo_vcr = vcr.VCR(
    cassette_library_dir='cassettes/seo/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseModelVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestMetaParametersAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestMetaParametersHistorialAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestSessionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test__session_data(self):
        pass
    

class TestUserCompanyVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserJourneyAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_user_link(self):
        pass
    

class TestUserPublicBlogVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserQuestionVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUserTermVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurCompanyVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurJourneyAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_user_link(self):
        pass
    

class TestVisiteurJourneyResource(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurPublicBlogVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurQuestionVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurTermVisitedAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestVisiteurUserRelationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
