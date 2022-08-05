from model_bakery import baker

from django.test import TestCase

from apps.socialmedias.socialposter.webpy import WebsiteContentCreation

from apps.web import constants
from apps.web.models import (
    WebsiteEmail, 
    WebsiteEmailsType, 
    WebsiteEmailTrack, 
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class TestTaks(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        return super().setUpTestData()
    
    def test_send_website_email_engagement(self):
        for user in User.objects.all():
            last_email_engagement = WebsiteEmailTrack.objects.filter(
                sent_to=user,
                email_related__sent=True,
                email_related__type_related__slug__startswith=constants.EMAIL_WEB_ENGAGEMENT
                )
            if (
                user.last_time_seen and
                (user.last_time_seen - last_email_engagement.date_to_send).days > 30
            ):
                email_to_send = WebsiteContentCreation.create_save_email(constants.CONTENT_FOR_ENGAGEMENT_USER_LITTLE_ACTIVE)
            elif not user.last_time_seen:
                email_to_send = WebsiteContentCreation.create_save_email(constants.CONTENT_FOR_ENGAGEMENT_USER_NO_ACTIVE)

            enviar_email_task.delay(email_to_send.dict_for_task, user.id, 'web')