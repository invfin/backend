import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.views import (
CreateQuestionView,
QuestionDetailsView,
QuestionsView,
UpdateQuestionView,
)

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/views/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCreateQuestionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form_invalid(self):
        pass
    
    def test_form_valid(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_get_initial(self):
        pass
    

class TestQuestionDetailsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_context_data(self):
        pass
    

class TestQuestionsView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestUpdateQuestionView(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form_valid(self):
        pass
    
    def test_get_context_data(self):
        pass
    
    def test_handle_no_permission(self):
        pass
    
    def test_test_func(self):
        pass
    
