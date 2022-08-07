import random

from django.contrib.auth import get_user_model

from model_bakery import baker

from apps.web import constants
from apps.web.models import (
    WebsiteEmail,
    WebsiteEmailsType,
    WebsiteEmailTrack,
    Promotion,
    PromotionCampaign
)


User = get_user_model()


class WebsiteEmailExample:
    def create_email_types(self):
        return [WebsiteEmailsType.objects.create(name=purposes[0]) for purposes in constants.CONTENT_PURPOSES]

    def create_emails(self, email_types: list):
        baker.make(
            WebsiteEmailTrack,
            email_related=baker.make(
                WebsiteEmail,
                type_related=random.choice(email_types)
            ),
            sent_to=baker.make(User)
        )

    @classmethod
    def create_examples(cls):
        email_types = cls().create_email_types()
        cls().create_emails(email_types)
