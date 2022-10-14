import vcr

from unittest.mock import patch

from bfet import DjangoTestingModel

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.socialmedias.outils.content_creation import ContentCreation
from apps.socialmedias import constants as social_constants
from apps.socialmedias.models import Emoji, DefaultTilte, DefaultContent
from apps.web import constants as web_constants
from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.preguntas_respuestas.models import Question


class TestContentCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.emoji_1 = DjangoTestingModel.create(Emoji)
        cls.default_title = DjangoTestingModel.create(DefaultTilte, title="Default title")
        cls.default_content = DjangoTestingModel.create(DefaultContent)

    def test_create_title(self):
        # Test with no emojis no custom title
        expected_data = {"title": "Custom title"}
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=False,
            use_emojis=False,
        )
        assert expected_data == result_data

        # Test with no emojis no custom title, no title
        expected_data = {
            "title": "Default title",
            "default_title": self.default_title,
        }
        result_data = ContentCreation.create_title(
            customize_title=False,
            use_emojis=False,
        )
        assert expected_data == result_data

        # Test with no emojis, custom title at the beginning and no filters
        expected_data = {
            "title": "Default title Custom title",
            "default_title": self.default_title,
        }
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=True,
            custom_title_info={
                "default_title_position": "Beginning",
                "default_title_filter": {},
            },
            use_emojis=False,
        )
        assert expected_data == result_data

        # Test with no emojis, custom title at the end and no filters
        expected_data = {
            "title": "Custom title Default title",
            "default_title": self.default_title,
        }
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=True,
            custom_title_info={
                "default_title_position": "End",
                "default_title_filter": {},
            },
            use_emojis=False,
        )
        assert expected_data == result_data

        # Test with one emoji and default title
        expected_data = {
            "title": f"{self.emoji_1} Default title",
            "default_title": self.default_title,
            "emojis": [self.emoji_1],
        }
        result_data = ContentCreation.create_title(
            customize_title=False,
            use_emojis=True,
            emojis_info={
                "emoji_1_position": "Beginning",
            },
        )
        assert expected_data == result_data

        # Test with one emoji and no custom title
        expected_data = {"title": f"Custom title {self.emoji_1}", "emojis": [self.emoji_1]}
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=False,
            use_emojis=True,
            emojis_info={
                "emoji_1_position": "End",
            },
        )
        assert expected_data == result_data

        # Test with one emoji and custom title
        expected_data = {
            "title": f"Custom title {self.emoji_1} Default title",
            "default_title": self.default_title,
            "emojis": [self.emoji_1],
        }
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=True,
            custom_title_info={
                "default_title_position": "End",
            },
            use_emojis=True,
            emojis_info={
                "emoji_1_position": "Middle",
            },
        )
        assert expected_data == result_data

        # Test with two emojis and custom title
        emoji_2 = DjangoTestingModel.create(Emoji)
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=True,
            custom_title_info={
                "default_title_position": "Beginning",
            },
            use_emojis=True,
            emojis_info={
                "emoji_1_position": "Beginning",
                "emoji_2_position": "End",
            },
        )
        assert ("Default title Custom title" in result_data["title"]) is True
        assert (self.emoji_1.emoji in result_data["title"]) is True
        assert (emoji_2.emoji in result_data["title"]) is True
        assert (self.emoji_1.emoji and emoji_2.emoji in result_data["title"]) is True
        assert (self.emoji_1 in result_data["emojis"]) is True
        assert (emoji_2 in result_data["emojis"]) is True
        assert (self.emoji_1 and emoji_2 in result_data["emojis"]) is True
        assert self.default_title == result_data["default_title"]

        # Test with three emojis and custom title
        emoji_3 = DjangoTestingModel.create(Emoji)
        result_data = ContentCreation.create_title(
            "Custom title",
            customize_title=True,
            custom_title_info={
                "default_title_position": "Beginning",
            },
            use_emojis=True,
            emojis_info={
                "emoji_1_position": "Beginning",
                "emoji_2_position": "Middle",
                "emoji_3_position": "End",
            },
        )
        assert ("Default title" in result_data["title"]) is True
        assert ("Custom title" in result_data["title"]) is True
        assert (self.emoji_1.emoji in result_data["title"]) is True
        assert (emoji_2.emoji in result_data["title"]) is True
        assert (emoji_3.emoji in result_data["title"]) is True
        assert (self.emoji_1.emoji and emoji_2.emoji and emoji_3.emoji in result_data["title"]) is True
        assert (self.emoji_1 in result_data["emojis"]) is True
        assert (emoji_2 in result_data["emojis"]) is True
        assert (emoji_3 in result_data["emojis"]) is True
        assert (self.emoji_1 and emoji_2 and emoji_3 in result_data["emojis"]) is True
        assert self.default_title == result_data["default_title"]

        # Test with no emojis, custom title filtered
        default_title_news = DjangoTestingModel.create(
            DefaultTilte, title="Default title news", for_content=social_constants.NEWS
        )
        expected_data = {
            "title": "Default title news",
            "default_title": default_title_news,
        }
        result_data = ContentCreation.create_title(
            customize_title=True,
            custom_title_info={
                "default_title_position": "Beginning",
                "default_title_filter": {"for_content": social_constants.NEWS},
            },
            use_emojis=False,
        )
        assert expected_data == result_data

    def test_create_content(self, web_content, web_filters):
        custom_content = "Custom custom_content"
        custom_dict = ContentCreation.create_content(custom_content)
        custom_expected_result = {"content": custom_content}
        assert custom_dict == custom_expected_result

        default_dict = ContentCreation.create_content(filter=web_filters)
        default_expected_result = {"content": web_content.content, "default_content": web_content}
        assert default_dict == default_expected_result
