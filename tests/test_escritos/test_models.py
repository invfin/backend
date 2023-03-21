from django.test import TestCase
from django.contrib.auth import get_user_model

from bfet import DjangoTestingModel

from src.escritos.models import TermContent, TermCorrection

User = get_user_model()


class TestTermContent(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term_content = TermContent(
            title="term title",
            content="term content",
        )
        cls.user = DjangoTestingModel.create(User)

    def test_populate_original(self):
        term_content = TermContent(
            title="term title",
            content="term content",
        )
        term_correction = TermCorrection(term_content_related=term_content)
        term_correction.populate_original()
        self.assertEqual(term_correction.original_title, "term title")
        self.assertEqual(term_correction.original_content, "term content")
