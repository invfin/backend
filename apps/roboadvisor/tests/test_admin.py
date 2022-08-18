import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.admin import (
InvestorProfileAdmin,
RoboAdvisorQuestionCompanyAnalysisAdmin,
RoboAdvisorQuestionFinancialSituationAdmin,
RoboAdvisorQuestionInvestorExperienceAdmin,
RoboAdvisorQuestionPortfolioAssetsWeightAdmin,
RoboAdvisorQuestionPortfolioCompositionAdmin,
RoboAdvisorQuestionRiskAversionAdmin,
RoboAdvisorQuestionStocksPortfolioAdmin,
RoboAdvisorServiceAdmin,
RoboAdvisorServiceStepAdmin,
RoboAdvisorServiceStepInline,
RoboAdvisorUserServiceActivityAdmin,
RoboAdvisorUserServiceStepActivityAdmin,
TemporaryInvestorProfileAdmin,
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestInvestorProfileAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionCompanyAnalysisAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionFinancialSituationAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionInvestorExperienceAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionPortfolioAssetsWeightAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionPortfolioCompositionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionRiskAversionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionStocksPortfolioAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorServiceAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorServiceStepAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorServiceStepInline(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorUserServiceActivityAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorUserServiceStepActivityAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestTemporaryInvestorProfileAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
