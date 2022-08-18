import vcr
from model_bakery import baker

from django.test import TestCase

from apps.recsys.views import (
BaseCompanyVisitedRecommendationView,
BaseRecommendationView,
CompaniesRecommendedSide,
ExplorationView,
RecommendationClickedRedirectView,
)

recsys_vcr = vcr.VCR(
    cassette_library_dir='cassettes/recsys/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseCompanyVisitedRecommendationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_generate_recommendations(self):
        pass
    
    def test_generate_recommendations_explanations(self):
        pass
    
    def test_get_companies_visited(self):
        pass
    
    def test_get_random_companies_recommendations(self):
        pass
    
    def test_get_specific_company_recommendations(self):
        pass
    

class TestBaseRecommendationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_create_recommendations(self):
        pass
    
    def test_generate_recommendations(self):
        pass
    
    def test_generate_recommendations_explanations(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_recommendation_log_model(self):
        pass
    
    def test_return_recommendations(self):
        pass
    

class TestCompaniesRecommendedSide(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestExplorationView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestRecommendationClickedRedirectView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_generate_url(self):
        pass
    
    def test_get_and_save_model(self):
        pass
    
    def test_get_redirect_url(self):
        pass
    
