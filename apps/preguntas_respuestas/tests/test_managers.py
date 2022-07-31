import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.managers import (
QuestionManager,
)

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/managers/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestQuestionManager(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_get_random(self):
        pass
    
