
from model_bakery import baker

from django.test import TestCase

from apps.socialmedias.socialposter.webpy import WebsiteContentCreation
from apps.socialmedias.models import DefaultContent, DefaultTilte, Emoji
from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.web.models import (
    WebsiteEmail, 
    WebsiteEmailsType, 
    WebsiteEmailTrack, 
    WebsiteLegalPage,
    Promotion,
    PromotionCampaign
)


class TestWebsiteContentCreation(TestCase):
    @classmethod
    def setUpClass(cls):
        import django
        django.setup()
        
    @classmethod
    def setUpTestData(cls) -> None:        
        cls.content = baker.make(DefaultContent, **cls.filters) 
        cls.title = baker.make(DefaultTilte, **cls.filters) 
        cls.emojis = baker.make(Emoji, 2)
        cls.filters = {
            "for_content": social_constants.WEB,
            "purpose": web_constants.CONTENT_FOR_ENGAGEMENT
        }
    
    def test_create_title(self):
        custom_title = "Custom title"
        custom_dict = WebsiteContentCreation().create_title(custom_title)
        custom_expected_result = {"title": custom_title}
        self.assertEqual(custom_dict, custom_expected_result)
        
        default_dict = WebsiteContentCreation().create_title(filter=self.filters)
        default_expected_result = {
            "title": self.title.title,
            "default_title": self.title
        }
        self.assertEqual(default_dict, default_expected_result)

    def test_create_content(self):
        custom_content = "Custom custom_content"
        custom_dict = WebsiteContentCreation().create_content(custom_content)
        custom_expected_result = {"content": custom_content}
        self.assertEqual(custom_dict, custom_expected_result)
        
        default_dict = WebsiteContentCreation().create_content(filter=self.filters)
        default_expected_result = {
            "content": self.content.content,
            "default_content": self.content
        }
        self.assertEqual(default_dict, default_expected_result)

    def test_create_emojis(self):
        self.assertEqual(
            self.emojis, 
            WebsiteContentCreation().create_emojis()
        )

    def test_create_save_email(self):
        WebsiteContentCreation.create_save_email()