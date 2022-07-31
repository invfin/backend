import vcr
from model_bakery import baker

from django.test import TestCase

from apps.preguntas_respuestas.forms import (
CreateAnswerForm,
CreateQuestionForm,
)
from apps.preguntas_respuestas.models import Answer, Question

from .data import QUESTION, ANSWER

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/preguntas_respuestas/forms/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestCreateAnswerForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_form(self):
        data = {"content": ANSWER["content"]}
        form = CreateAnswerForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()

class TestCreateQuestionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass
    
    def test_clean_content(self):
        form = CreateQuestionForm(data={"title": "No quesiton mark"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["title"], 
            "Añade puntuación a tu pregunta ¿ ?"
        )

        form = CreateQuestionForm(data={"title": "¿Cuál es tu pregunta?"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["title"], 
            "Formula tu pregunta para que la comunidad pueda ayudarte"
        )

        form = CreateQuestionForm(data={"title": "¿hey?"})
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors["title"], 
            "Formula tu pregunta para que la comunidad pueda ayudarte"
        )
    
    def test_clean_title(self):
        form = CreateQuestionForm(data={"content": "Mini"})
        self.assertTrue(form.is_valid())
        self.assertEqual(
            form.errors["content"], 
            "Detalla precisamente tu pregunta para que la comunidad pueda ayudarte."
        )
    
