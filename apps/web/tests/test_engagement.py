import pytest

from bfet import DjangoTestingModel as DTM

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


pytestmark = pytest.mark.django_db


class TestEngagementMachine:

    def test_send_website_email_engagement(self):
        pass
