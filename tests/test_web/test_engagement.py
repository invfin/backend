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


from django.test import TestCase


from django.test import TestCase


class TestEngagementMachine(TestCase):
    def test_send_website_email_engagement(self):
        pass
