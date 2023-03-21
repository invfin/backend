from datetime import datetime, timezone

from django.test import TestCase
from django.contrib.auth import get_user_model

from freezegun import freeze_time
from bfet import DjangoTestingModel

from src.escritos.models import TermContent, TermCorrection, Term
from src.escritos.outils.term_correction import TermCorrectionManagement

User = get_user_model()


class TestTermCorrectionManagement(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term_content = TermContent(
            title="term title",
            content="term content",
        )
        cls.user = DjangoTestingModel.create(User)

    def test_create_content(self):
        term_content = TermContent(
            term_related=Term(slug="term slug"),
            title="term title",
            content="term content",
        )
        term_correction = TermCorrection(
            term_content_related=term_content,
            title="new title",
        )
        print(TermCorrectionManagement(term_correction).create_content())
        self.assertEqual(
            TermCorrectionManagement(term_correction).create_content(),
            "Enhorabuena, tu correción para <a href='http://example.com:8000/definicion/term%20slug/#term-title' target='_blank'>new title</a> ha sido aprovada.<br></br>Desde el equipo de InvFin te damos las gracias por ayudar a mejorar el contenido para poder seguir ayudando al resto de la comunidad.",
        )


    @freeze_time("2022-04-01 13:30")
    def test_update_correction_data_when_approved(self):
        term_content = TermContent.objects.create(
            title="term title",
            content="term content",
        )
        term_correction = TermCorrection.objects.create(
            term_content_related=term_content,
            title="new title",
        )
        TermCorrectionManagement(term_correction).update_correction_data_when_approved(self.user, ["title"])
        term_correction.refresh_from_db()
        self.assertEqual(term_correction.title, "new title")
        self.assertEqual(term_correction.is_approved, True)
        self.assertEqual(term_correction.approved_by, self.user)
        self.assertEqual(
            term_correction.date_approved,
            datetime(2022, 4, 1, 13, 30, tzinfo=timezone.utc),
        )

    def test_replace_content_with_correction(self):
        term_content = TermContent.objects.create(
            title="term title",
            content="term content",
        )
        term_correction = TermCorrection.objects.create(
            term_content_related=term_content,
            title="new title",
            content="term content",
        )
        TermCorrectionManagement(term_correction).replace_content_with_correction(["title", "content"])
        term_content.refresh_from_db()
        self.assertEqual(term_content.title, "new title")
        self.assertEqual(term_content.content, "term content")

    def test_update_related_field_none_field(self):
        term_correction = TermCorrection(title="new title")
        self.assertEqual(
            TermCorrectionManagement(term_correction).update_related_field("title"),
            None,
        )

    def test_update_related_field_original_is_current(self):
        term_content = TermContent(title="new title")
        term_correction = TermCorrection(
            term_content_related=term_content,
            title="new title",
        )
        self.assertEqual(
            TermCorrectionManagement(term_correction).update_related_field("title"),
            None,
        )

    def test_update_related_field(self):
        term_correction = TermCorrection(
            term_content_related=self.term_content,
            title="new title",
        )
        self.assertEqual(
            TermCorrectionManagement(term_correction).update_related_field("title"),
            "title",
        )
