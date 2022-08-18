import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.models import (
BaseInvestorProfile,
BaseRoboAdvisorHorizon,
BaseRoboAdvisorQuestion,
BaseRoboAdvisorQuestionAsset,
InvestorProfile,
RoboAdvisorQuestionCompanyAnalysis,
RoboAdvisorQuestionFinancialSituation,
RoboAdvisorQuestionInvestorExperience,
RoboAdvisorQuestionPortfolioAssetsWeight,
RoboAdvisorQuestionPortfolioComposition,
RoboAdvisorQuestionRiskAversion,
RoboAdvisorQuestionStocksPortfolio,
RoboAdvisorService,
RoboAdvisorServiceStep,
RoboAdvisorUserServiceActivity,
RoboAdvisorUserServiceStepActivity,
TemporaryInvestorProfile,
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseInvestorProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestBaseRoboAdvisorHorizon(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestBaseRoboAdvisorQuestion(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestBaseRoboAdvisorQuestionAsset(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestInvestorProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestRoboAdvisorQuestionCompanyAnalysis(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionFinancialSituation(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionInvestorExperience(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionPortfolioAssetsWeight(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionPortfolioComposition(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionRiskAversion(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionStocksPortfolio(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorService(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
    def test_save(self):
        pass
    

class TestRoboAdvisorServiceStep(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_save(self):
        pass
    

class TestRoboAdvisorUserServiceActivity(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestRoboAdvisorUserServiceStepActivity(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestTemporaryInvestorProfile(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
