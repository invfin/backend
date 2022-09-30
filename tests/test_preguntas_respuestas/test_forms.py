import vcr
import pytest

from bfet import DjangoTestingModel as DTM

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
pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class TestCreateAnswerForm:
    @classmethod
    def setup_class(cls):
        pass

    def test_form(self):
        data = {"content": ANSWER["content"]}
        form = CreateAnswerForm(data=data)
        assert form.is_valid() is True
        form.save()


@pytest.mark.django_db
class TestCreateQuestionForm:
    @classmethod
    def setup_class(cls):
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
