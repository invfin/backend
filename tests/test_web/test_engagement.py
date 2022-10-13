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
from apps.socialmedias.outils.content_creation import ContentCreation
from apps.web.outils.engagement import EngagementMachine
from apps.web.models import WebsiteEmail, WebsiteEmailsType
from apps.socialmedias import constants as social_constants


@pytest.mark.django_db
@pytest.mark.django_db
class TestEngagementMachine:
    def test_send_website_email_engagement(self):
        pass

    def test_create_save_email(self):
        web_email_type = constants.CONTENT_FOR_ENGAGEMENT
        base_filters = {"for_content": social_constants.WEB, "purpose": web_email_type}

        title_filter = {}
        content_filter = {}
        title_filter.update(base_filters)
        content_filter.update(base_filters)

        title_dict = ContentCreation.create_title(None, title_filter)  # TODO fix
        content_dict = ContentCreation.create_content(None, content_filter)
        first_emoji, last_emoji = ContentCreation.create_emojis()

        title = title_dict["title"]
        title_dict["title"] = f"{first_emoji}{title}{last_emoji}"
        type_related, created = WebsiteEmailsType.objects.get_or_create(slug=web_email_type)

        expected_web_email = WebsiteEmail.objects.create(
            type_related=type_related,
            **title_dict,
            **content_dict,
        )
        expected_web_email.title_emojis.add(first_emoji, last_emoji)

        web_email = EngagementMachine.create_save_email(web_email_type)

        assert expected_web_email.title == web_email.title
        assert expected_web_email.content == web_email.content
        assert expected_web_email.default_title == web_email.default_title
        assert expected_web_email.default_content == web_email.default_content
        assert expected_web_email.title_emojis == web_email.title_emojis
        assert expected_web_email.sent == web_email.sent
        assert expected_web_email.date_to_send == web_email.date_to_send
