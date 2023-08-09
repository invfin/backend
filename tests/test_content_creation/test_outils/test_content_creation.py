from django.test import TestCase

from bfet import DjangoTestingModel, create_random_string

from src.content_creation import constants
from src.content_creation.models import DefaultContent, DefaultTilte, Emoji, Hashtag
from src.content_creation.outils.content_creator import ContentCreation
from src.socialmedias import constants as social_constants


class TestContentCreation(TestCase):
    def setUp(self) -> None:
        self.content_creator = ContentCreation

    def test_create_hashtags(self):
        # TODO create subtests for each socialmedia with hashtags
        hashtags = [
            DjangoTestingModel.create(
                Hashtag,
                title=create_random_string(20),
                platform=social_constants.FACEBOOK,
            )
            for index in range(2)
        ]
        data_result_list, data_result_hashtags = self.content_creator.create_hashtags(
            social_constants.FACEBOOK
        )
        assert data_result_hashtags == "#" + " #".join([hashtag.title for hashtag in hashtags])
        assert data_result_list == hashtags

        data_no_result_list, data_no_result_hashtags = self.content_creator.create_hashtags(
            social_constants.TWITTER
        )
        assert data_no_result_list == []
        assert data_no_result_hashtags == ""

    def test_create_utm_url(self):
        utm_params = dict(
            utm_source="utm_source",
            utm_medium="utm_medium",
            utm_campaign="utm_campaign",
            utm_term="utm term",
            slugify_term=True,
            link="link",
        )
        expected_url = "link?utm_source=utm_source&utm_medium=utm_medium&utm_campaign=utm_campaign&utm_term=utm-term"
        assert self.content_creator.create_utm_url(**utm_params) == expected_url

    def test_create_title(self):
        with self.subTest("Test with no emojis no custom title"):
            default_title = DjangoTestingModel.create(DefaultTilte, title="Default title")
            expected_data = {"title": "Custom title"}
            result_data = self.content_creator.create_title(
                "Custom title",
                customize_title=False,
                use_emojis=False,
            )
            assert expected_data == result_data

        with self.subTest("Test with no emojis no custom title, no title"):
            expected_data = {
                "title": "Default title",
                "default_title": default_title,
            }
            result_data = self.content_creator.create_title(
                customize_title=False,
                use_emojis=False,
            )
            assert expected_data == result_data

        with self.subTest("Test with no emojis, custom title at the beginning and no filters"):
            expected_data = {
                "title": "Default title Custom title",
                "default_title": default_title,
            }
            result_data = self.content_creator.create_title(
                "Custom title",
                customize_title=True,
                custom_title_info={
                    "default_title_position": "Beginning",
                    "default_title_filter": {},
                },
                use_emojis=False,
            )
            assert expected_data == result_data

        with self.subTest("Test with no emojis, custom title at the end and no filters"):
            expected_data = {
                "title": "Custom title Default title",
                "default_title": default_title,
            }
            result_data = self.content_creator.create_title(
                "Custom title",
                customize_title=True,
                custom_title_info={
                    "default_title_position": "End",
                    "default_title_filter": {},
                },
                use_emojis=False,
            )
            assert expected_data == result_data

        with self.subTest("Test with one emoji and default title"):
            emoji_1 = DjangoTestingModel.create(Emoji)
            expected_data = {
                "title": f"{emoji_1} Default title",
                "title_emojis": [emoji_1],
                "default_title": default_title,
            }
            result_data = self.content_creator.create_title(
                customize_title=False,
                use_emojis=True,
                emojis_info={
                    "emoji_1_position": "Beginning",
                },
            )
            assert expected_data == result_data

        with self.subTest("Test with one emoji and no custom title"):
            expected_data = {"title": f"Custom title {emoji_1}", "title_emojis": [emoji_1]}
            result_data = self.content_creator.create_title(
                "Custom title",
                customize_title=False,
                use_emojis=True,
                emojis_info={
                    "emoji_1_position": "End",
                },
            )
            assert expected_data == result_data

        with self.subTest("Test with one emoji and custom title"):
            expected_data = {
                "title": f"Custom title {emoji_1} Default title",
                "default_title": default_title,
                "title_emojis": [emoji_1],
            }
            result_data = self.content_creator.create_title(
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

        with self.subTest("Test with two emojis and custom title"):
            emoji_2 = DjangoTestingModel.create(Emoji)
            result_data = self.content_creator.create_title(
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
            assert (emoji_1.emoji in result_data["title"]) is True
            assert (emoji_2.emoji in result_data["title"]) is True
            assert (emoji_1.emoji and emoji_2.emoji in result_data["title"]) is True
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_2 in result_data["title_emojis"]) is True
            assert (emoji_1 and emoji_2 in result_data["title_emojis"]) is True
            assert default_title == result_data["default_title"]

        with self.subTest("Test with three emojis and custom title"):
            emoji_3 = DjangoTestingModel.create(Emoji)
            result_data = self.content_creator.create_title(
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
            assert (emoji_1.emoji in result_data["title"]) is True
            assert (emoji_2.emoji in result_data["title"]) is True
            assert (emoji_3.emoji in result_data["title"]) is True
            assert (
                emoji_1.emoji and emoji_2.emoji and emoji_3.emoji in result_data["title"]
            ) is True
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_2 in result_data["title_emojis"]) is True
            assert (emoji_3 in result_data["title_emojis"]) is True
            assert (emoji_1 and emoji_2 and emoji_3 in result_data["title_emojis"]) is True
            assert default_title == result_data["default_title"]

        with self.subTest("Test with no emojis, custom title filtered"):
            default_title_news = DjangoTestingModel.create(
                DefaultTilte, title="Default title news", for_content=constants.NEWS
            )
            expected_data = {
                "title": "Default title news",
                "default_title": default_title_news,
            }
            result_data = self.content_creator.create_title(
                customize_title=True,
                custom_title_info={
                    "default_title_position": "Beginning",
                    "default_title_filter": {"for_content": constants.NEWS},
                },
                use_emojis=False,
            )
            assert expected_data == result_data

    def test_create_random_title(self):
        emoji_1 = DjangoTestingModel.create(Emoji)
        default_title = DjangoTestingModel.create(DefaultTilte, title="Default title")
        result_data = self.content_creator.create_random_title()
        expected_data = {
            "title": "Default title",
            "default_title": default_title,
        }
        if "title_emojis" in result_data:
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
            assert default_title == result_data["default_title"]
        else:
            assert result_data == expected_data

        default_title_news = DjangoTestingModel.create(
            DefaultTilte, title="Default title news", for_content=constants.NEWS
        )
        result_data = self.content_creator.create_random_title(
            **{"default_title_filter": {"for_content": constants.NEWS}},
        )
        expected_data = {
            "title": "Default title news",
            "default_title": default_title_news,
        }
        if "title_emojis" in result_data:
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
            assert default_title_news == result_data["default_title"]
        else:
            assert result_data == expected_data

        result_data = self.content_creator.create_random_title(**{"title": "Custom title"})
        if "title_emojis" in result_data:
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        if "default_title" in result_data:
            if result_data["default_title"].title.endswith("news"):
                assert default_title_news == result_data["default_title"]
            else:
                assert default_title == result_data["default_title"]
        else:
            expected_data = {"title": "Custom title"}
            assert result_data == expected_data

    def test_create_content(self):
        default_content = DjangoTestingModel.create(DefaultContent)
        assert self.content_creator.create_content() == {
            "content": default_content.content,
            "default_content": default_content,
        }

        assert self.content_creator.create_content(content="first content") == {
            "content": "first content"
        }

        DjangoTestingModel.create(DefaultContent, for_content=constants.WEB)

        assert self.content_creator.create_content(
            content="first content",
            default_content_filter={"for_content__in": [constants.WEB]},
        ) == {
            "content": "first content",
        }
