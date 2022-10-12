import vcr
import pytest

from bfet import DjangoTestingModel

from apps.preguntas_respuestas.forms import (
    CreateAnswerForm,
    CreateQuestionForm,
)
from apps.preguntas_respuestas.models import Answer, Question

from tests.data.preguntas_respuestas_data import QUESTION, ANSWER

preguntas_respuestas_vcr = vcr.VCR(
    cassette_library_dir="cassettes/preguntas_respuestas/forms/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


from django.test import TestCase


class TestCreateAnswerForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_form(self):
        data = {"content": ANSWER["content"]}
        form = CreateAnswerForm(data=data)
        assert form.is_valid() is True
        form.save()


from django.test import TestCase


class TestCreateQuestionForm(TestCase):
    @classmethod
    def setUpTestData(cls):
        pass

    def test_clean_content(self):
        form = CreateQuestionForm(data={"title": "¿Cuál es tu pregunta?"})
        assert form.is_valid() is True
        assert form.errors["title"] == "Formula tu pregunta para que la comunidad pueda ayudarte"

        form = CreateQuestionForm(data={"title": "¿hey?"})
        assert form.is_valid()
        assert form.errors["title"] == "Formula tu pregunta para que la comunidad pueda ayudarte"

    def test_clean_title(self):
        form = CreateQuestionForm(data={"content": "Mini"})
        self.assertTrue(form.is_valid())
        assert form.errors["content"] == "Detalla precisamente tu pregunta para que la comunidad pueda ayudarte."
