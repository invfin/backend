from apps.bfet import ExampleModel

from django.test import TestCase

from apps.web import constants
from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailsType,
    WebsiteEmailTrack,
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign,
)
from apps.web.outils.content_creation import WebsiteContentCreation
from apps.web.outils.engagement import EngagementMachine


class TestEngagementMachine(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        ExampleModel.create


    def test_send_website_email_engagement(self):
        pass
