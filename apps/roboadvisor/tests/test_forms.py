import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.forms import (
BaseRoboAdvisorForm,
RoboAdvisorQuestionCompanyAnalysisForm,
RoboAdvisorQuestionFinancialSituationForm,
RoboAdvisorQuestionInvestorExperienceForm,
RoboAdvisorQuestionPortfolioAssetsWeightForm,
RoboAdvisorQuestionPortfolioCompositionForm,
RoboAdvisorQuestionRiskAversionForm,
RoboAdvisorQuestionStocksPortfolioForm,
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestBaseRoboAdvisorForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_range_values(self):
        pass
    

class TestRoboAdvisorQuestionCompanyAnalysisForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionFinancialSituationForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionInvestorExperienceForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___init__(self):
        pass
    

class TestRoboAdvisorQuestionPortfolioAssetsWeightForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionPortfolioCompositionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestRoboAdvisorQuestionRiskAversionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___init__(self):
        pass
    

class TestRoboAdvisorQuestionStocksPortfolioForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
