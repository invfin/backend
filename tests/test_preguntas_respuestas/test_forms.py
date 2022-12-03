from django.test import TestCase

from src.preguntas_respuestas.forms import CreateQuestionForm


class TestCreateQuestionForm(TestCase):
    def test_clean_content(self):
        form = CreateQuestionForm(data={"title": "¿Es esto una pregunta largar?", "content": "Mini"})
        assert form.is_valid() is False
        assert (
            "Detalla precisamente tu pregunta para que la comunidad pueda ayudarte." in form.errors["content"]
        ) is True

    def test_clean_title(self):
        form = CreateQuestionForm(data={"title": "¿Cuál es tu pregunta?"})
        assert form.is_valid() is False
        assert ("Formula tu pregunta para que la comunidad pueda ayudarte" in form.errors["title"]) is True

        form = CreateQuestionForm(data={"title": "¿hey?"})
        assert form.is_valid() is False
        assert ("Formula tu pregunta para que la comunidad pueda ayudarte" in form.errors["title"]) is True
