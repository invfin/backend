from django.contrib.auth import get_user_model
from django.test import TestCase

from bfet import DjangoTestingModel

from src.escritos.models import Term, TermContent, TermCorrection

User = get_user_model()


class TestTermCorrectionQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term = DjangoTestingModel.create(Term)
        cls.user = DjangoTestingModel.create(User, email="1@gmal.com", is_writer=False)
        cls.user_2 = DjangoTestingModel.create(User, email="2@gmal.com", is_writer=False)
        cls.term_content = TermContent.objects.create(
            term_related=cls.term,
            title="term title",
            content="term content",
        )
        cls.term_content_2 = TermContent.objects.create(
            term_related=cls.term,
            title="term title",
            content="term content",
        )
        cls.correction_approved = DjangoTestingModel.create(
            TermCorrection,
            term_content_related=cls.term_content,
            corrected_by=cls.user,
            is_approved=True,
        )
        cls.correction_approved_2 = DjangoTestingModel.create(
            TermCorrection,
            term_content_related=cls.term_content,
            corrected_by=cls.user_2,
            is_approved=True,
        )
        cls.correction_approved_duplicated = DjangoTestingModel.create(
            TermCorrection,
            term_content_related=cls.term_content_2,
            corrected_by=cls.user,
            is_approved=True,
        )

    def test_get_contributors(self):
        result = [_.corrected_by for _ in TermCorrection.objects.get_contributors(self.term)]
        self.assertEqual(len(result), 2)
        self.assertIn(self.user, result)
        self.assertIn(self.user_2, result)
