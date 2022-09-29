from bfet import DjangoTestingModel as DTM

import pytest

from django.test import TestCase 

pytestmark = pytest.mark.django_db

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
        DTM.create


    def test_send_website_email_engagement(self):
        pass
