import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.views import (
RoboAdvisorResultView,
RoboAdvisorServiceOptionView,
RoboAdvisorServicesListView,
RoboAdvisorUserResultsListView,
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestRoboAdvisorResultView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestRoboAdvisorServiceOptionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_prepare_forms(self):
        pass
    

class TestRoboAdvisorServicesListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestRoboAdvisorUserResultsListView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_queryset(self):
        pass
    
