from unittest.mock import patch

from django.test import TestCase

from apps.web.outils.content_creation import WebsiteContentCreation

from apps.web import constants
from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailsType,
    WebsiteEmailTrack,
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class TestTasks(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()

    def test_send_website_email_engagement(self, mock_test_task):
        pass
