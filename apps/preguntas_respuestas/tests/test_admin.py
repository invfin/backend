import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.admin import (
AnswerAdmin,
AnswerCommentAdmin,
QuesitonCommentAdmin,
QuestionAdmin,
)

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/admin/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestAnswerAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestAnswerCommentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestQuesitonCommentAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    

class TestQuestionAdmin(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
