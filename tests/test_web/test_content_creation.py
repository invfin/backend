import pytest


from apps.web.outils.content_creation import WebsiteContentCreation
from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail, WebsiteEmailsType


@pytest.mark.django_db
class TestWebsiteContentCreation:
    def test_create_title(self, web_title, web_filters):
        custom_title = "Custom title"
        custom_dict = WebsiteContentCreation.create_title(custom_title)
        custom_expected_result = {"title": custom_title}
        assert custom_dict == custom_expected_result

        default_dict = WebsiteContentCreation.create_title(filter=web_filters)
        default_expected_result = {"title": web_title.title, "default_title": web_title}
        assert default_dict == default_expected_result

    def test_create_content(self, web_content, web_filters):
        custom_content = "Custom custom_content"
        custom_dict = WebsiteContentCreation.create_content(custom_content)
        custom_expected_result = {"content": custom_content}
        assert custom_dict == custom_expected_result

        default_dict = WebsiteContentCreation.create_content(filter=web_filters)
        default_expected_result = {"content": web_content.content, "default_content": web_content}
        assert default_dict == default_expected_result

    def test_create_emojis(self, web_emojis):
        emoji_1, emoji_2 = WebsiteContentCreation.create_emojis()
        assert emoji_1 in web_emojis
        assert emoji_2 in web_emojis

    def test_create_save_email(self):
        web_email_type = web_constants.CONTENT_FOR_ENGAGEMENT
        base_filters = {"for_content": social_constants.WEB, "purpose": web_email_type}

        title_filter = {}
        content_filter = {}
        title_filter.update(base_filters)
        content_filter.update(base_filters)

        title_dict = WebsiteContentCreation.create_title(None, title_filter)
        content_dict = WebsiteContentCreation.create_content(None, content_filter)
        first_emoji, last_emoji = WebsiteContentCreation.create_emojis()

        title = title_dict["title"]
        title_dict["title"] = f"{first_emoji}{title}{last_emoji}"
        type_related, created = WebsiteEmailsType.objects.get_or_create(slug=web_email_type)

        expected_web_email = WebsiteEmail.objects.create(
            type_related=type_related,
            **title_dict,
            **content_dict,
        )
        expected_web_email.title_emojis.add(first_emoji, last_emoji)

        web_email = WebsiteContentCreation.create_save_email(web_email_type)

        assert expected_web_email.title == web_email.title
        assert expected_web_email.content == web_email.content
        assert expected_web_email.default_title == web_email.default_title
        assert expected_web_email.default_content == web_email.default_content
        assert expected_web_email.title_emojis == web_email.title_emojis
        assert expected_web_email.sent == web_email.sent
        assert expected_web_email.date_to_send == web_email.date_to_send
