from model_bakery import baker

from django.core import mail
from django.test import TestCase

from apps.general.outils.emailing import EmailingSystem
from apps.public_blog.models import EmailPublicBlog
from apps.general.models import EmailNotification
from apps.general import constants as web_constants
from apps.web.models import (
    WebsiteEmail, 
    WebsiteEmailsType, 
    WebsiteEmailTrack, 
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class TestEmailingSystem(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.email_public_blog = baker.make(EmailPublicBlog)
        cls.email_notif = baker.make(EmailNotification)
        cls.website_email = baker.make(WebsiteEmail)
        cls.email_sys_pb = EmailingSystem(is_for=web_constants.EMAIL_FOR_NEWSLETTER)
        cls.email_sys_notif = EmailingSystem(is_for=web_constants.EMAIL_FOR_NOTIFICATION)
        cls.email_sys_web = EmailingSystem(is_for=web_constants.EMAIL_FOR_WEB)
 
    def test_prepare_email_track(self):
        self.email_sys_pb.prepare_email_track()
        self.email_sys_notif.prepare_email_track()
        self.email_sys_web.prepare_email_track()

    def test_prepare_email(self):
        pass

    def test_prepare_sender(self):
        pass

    def test_prepare_message(self):
        pass

    def test_enviar_email(self):
        pass
