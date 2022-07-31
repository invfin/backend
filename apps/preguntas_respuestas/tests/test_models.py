import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.models import (
Answer,
AnswerComment,
QuesitonComment,
Question,
)

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/models/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAnswer(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    

class TestAnswerComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestQuesitonComment(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    

class TestQuestion(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test___str__(self):
        pass
    
    def test_add_answer(self):
        pass
    
    def test_get_absolute_url(self):
        pass
    
