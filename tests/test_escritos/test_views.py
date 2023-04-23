from django.test import TestCase

from src.escritos.models import TermContent
from src.escritos.views import ManageUserTermCorrectionDetailView


class TestManageUserTermCorrectionDetailView(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term_content = TermContent(
            title="term title",
            content="term content",
        )

    def test_get_fields(self):
        self.assertEqual(
            ManageUserTermCorrectionDetailView.get_fields({"accept-title": "tilte", "not-here": "nop"}),
            ["title"],
        )
