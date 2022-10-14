import pytest


from apps.socialmedias.outils.content_creation import ContentCreation
from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail, WebsiteEmailsType


@pytest.mark.django_db
class TestContentCreation:
    def test_create_title(self, web_title, web_filters):
        custom_title = "Custom title"
        custom_dict = ContentCreation.create_title(custom_title)
        custom_expected_result = {"title": custom_title}
        assert custom_dict == custom_expected_result

        default_dict = ContentCreation.create_title(filter=web_filters)
        default_expected_result = {"title": web_title.title, "default_title": web_title}
        assert default_dict == default_expected_result

    def test_create_content(self, web_content, web_filters):
        custom_content = "Custom custom_content"
        custom_dict = ContentCreation.create_content(custom_content)
        custom_expected_result = {"content": custom_content}
        assert custom_dict == custom_expected_result

        default_dict = ContentCreation.create_content(filter=web_filters)
        default_expected_result = {"content": web_content.content, "default_content": web_content}
        assert default_dict == default_expected_result
