from model_bakery import baker

from django.core import mail
from django.test import TestCase

from apps.web.models import (
    WebsiteEmail, 
    WebsiteEmailsType, 
    WebsiteEmailTrack, 
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class TestContactForm(TestCase):
    pass