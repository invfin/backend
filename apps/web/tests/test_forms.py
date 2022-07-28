from model_bakery import baker

from django.test import TestCase

from apps.web.models import (
    WebsiteEmail, 
    WebsiteEmailsType, 
    WebsiteEmailTrack, 
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class FormTest(TestCase):
    pass