from bfet import DjangoTestingModel, DataCreator

from django.test import TestCase

from apps.escritos.models import Term
from apps.socialmedias.outils.content_creation import ContentCreation
from apps.socialmedias import constants as social_constants
from apps.socialmedias.models import Emoji, DefaultTilte, DefaultContent, TermSharedHistorial, Hashtag


class TestContentCreation(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term = DjangoTestingModel.create(Term)

    def test_get_object(self):
        content_creator = ContentCreation
        content_creator.model_class = Term

        assert content_creator().get_object() == self.term

    def test_get_shared_model_historial(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        content_creator.shared_model_historial = TermSharedHistorial
        assert content_creator().get_shared_model_historial() == TermSharedHistorial

        content_creator.shared_model_historial = None
        assert content_creator().get_shared_model_historial() == TermSharedHistorial

    def test_get_object_title(self):
        content_creator = ContentCreation
        content_creator.model_class = Term

        assert self.term.title == content_creator().get_object_title()

    def test_get_object_content(self):
        content_creator = ContentCreation
        content_creator.model_class = Term

        assert self.term.resume == content_creator().get_object_content()

    def test_get_object_media(self):
        content_creator = ContentCreation
        content_creator.model_class = Term

        assert self.term.image == content_creator().get_object_media()

    def test_create_hashtags(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        hashtags = DjangoTestingModel.create(
            Hashtag,
            quantity=2,
            in_bulk=True,
            title=DataCreator.create_random_string(20),
            platform=social_constants.FACEBOOK,
        )
        data_result_list, data_result_hashtags = content_creator.create_hashtags(social_constants.FACEBOOK)
        assert data_result_hashtags == "#" + " #".join([hashtag.title for hashtag in hashtags])
        assert data_result_list == list(hashtags)

        data_no_result_list, data_no_result_hashtags = content_creator.create_hashtags(social_constants.TWITTER)
        assert data_no_result_list == []
        assert data_no_result_hashtags == ""

    def test_create_utm_url(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        utm_params = dict(
            utm_source="utm_source",
            utm_medium="utm_medium",
            utm_campaign="utm_campaign",
            utm_term="utm term",
            slugify_term=True,
            link="link",
        )
        expected_url = "link?utm_source=utm_source&utm_medium=utm_medium&utm_campaign=utm_campaign&utm_term=utm-term"
        assert content_creator.create_utm_url(**utm_params) == expected_url

    def test_create_title(self):
        with self.subTest("Test with no emojis no custom title"):
            default_title = DjangoTestingModel.create(DefaultTilte, title="Default title")
            expected_data = {"title": "Custom title"}
            result_data = ContentCreation.create_title(
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
            result_data = ContentCreation.create_title(
                customize_title=False,
                use_emojis=False,
            )
            assert expected_data == result_data

        with self.subTest("Test with no emojis, custom title at the beginning and no filters"):
            expected_data = {
                "title": "Default title Custom title",
                "default_title": default_title,
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

        with self.subTest("Test with no emojis, custom title at the end and no filters"):
            expected_data = {
                "title": "Custom title Default title",
                "default_title": default_title,
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

        with self.subTest("Test with one emoji and default title"):
            emoji_1 = DjangoTestingModel.create(Emoji)
            expected_data = {
                "title": f"{emoji_1} Default title",
                "title_emojis": [emoji_1],
                "default_title": default_title,
            }
            result_data = ContentCreation.create_title(
                customize_title=False,
                use_emojis=True,
                emojis_info={
                    "emoji_1_position": "Beginning",
                },
            )
            assert expected_data == result_data

        with self.subTest("Test with one emoji and no custom title"):
            expected_data = {"title": f"Custom title {emoji_1}", "title_emojis": [emoji_1]}
            result_data = ContentCreation.create_title(
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

        with self.subTest("Test with two emojis and custom title"):
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
            assert (emoji_1.emoji in result_data["title"]) is True
            assert (emoji_2.emoji in result_data["title"]) is True
            assert (emoji_1.emoji and emoji_2.emoji in result_data["title"]) is True
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_2 in result_data["title_emojis"]) is True
            assert (emoji_1 and emoji_2 in result_data["title_emojis"]) is True
            assert default_title == result_data["default_title"]

        with self.subTest("Test with three emojis and custom title"):
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
            assert (emoji_1.emoji in result_data["title"]) is True
            assert (emoji_2.emoji in result_data["title"]) is True
            assert (emoji_3.emoji in result_data["title"]) is True
            assert (emoji_1.emoji and emoji_2.emoji and emoji_3.emoji in result_data["title"]) is True
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_2 in result_data["title_emojis"]) is True
            assert (emoji_3 in result_data["title_emojis"]) is True
            assert (emoji_1 and emoji_2 and emoji_3 in result_data["title_emojis"]) is True
            assert default_title == result_data["default_title"]

        with self.subTest("Test with no emojis, custom title filtered"):
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

    def test_create_url(self):
        content_creator = ContentCreation
        content_creator.model_class = Term

        assert content_creator().create_url() == self.term.shareable_link

    def test_create_content(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        default_content = DjangoTestingModel.create(DefaultContent)
        assert content_creator.create_content() == {
            "content": default_content.content,
            "default_content": default_content,
        }

        assert content_creator.create_content(content="first content") == {"content": "first content"}

        default_content_web = DjangoTestingModel.create(DefaultContent, for_content=social_constants.WEB)

        assert content_creator.create_content(
            content="first content",
            default_content_filter={"for_content__in": [social_constants.WEB]},
        ) == {
            "content": "first content",
        }

    def test_create_default_title_filter(self):
        with self.subTest("content All"):
            content_creator_all = ContentCreation
            content_creator_all.model_class = Term
            content_creator_all.for_content = []
            assert content_creator_all().create_default_title_filter() == {"for_content__in": [social_constants.ALL]}
        with self.subTest("content Term"):
            content_creator_term = ContentCreation
            content_creator_term.for_content = []
            content_creator_term.for_content = [social_constants.TERM]
            assert content_creator_term().create_default_title_filter() == {
                "for_content__in": [social_constants.ALL, social_constants.TERM]
            }
        with self.subTest("content with Web"):
            content_creator_web = ContentCreation
            content_creator_web.model_class = Term
            content_creator_web.for_content = []
            assert content_creator_web(social_constants.PLATFORM_WEB).create_default_title_filter() == {
                "for_content__in": [social_constants.ALL, social_constants.WEB]
            }

    def test_create_default_content_filter(self):
        assert ContentCreation().create_default_content_filter() == {"for_content__in": [social_constants.ALL]}

        assert ContentCreation(social_constants.PLATFORM_WEB).create_default_content_filter() == {
            "for_content__in": [social_constants.ALL, social_constants.WEB]
        }

    def test_prepare_inital_data(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        emoji_1 = DjangoTestingModel.create(Emoji)

        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=social_constants.ALL,
        )
        result_data = content_creator().prepare_inital_data()
        assert default_title_all == result_data["default_title"]
        assert self.term.resume == result_data["content"]
        assert self.term == result_data["content_shared"]
        if "title_emojis" in result_data:
            # Emoji might or might not be here because it's randomly generated
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        assert (default_title_all.title in result_data["title"]) is True
        assert self.term.shareable_link == result_data["link"]

    def test_create_newsletter_content_from_object(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        emoji_1 = DjangoTestingModel.create(Emoji)

        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=social_constants.ALL,
        )
        result_data = content_creator().create_newsletter_content_from_object()
        assert default_title_all == result_data["default_title"]
        assert self.term.resume == result_data["content"]
        assert self.term == result_data["content_shared"]
        if "title_emojis" in result_data:
            # Emoji might or might not be here because it's randomly generated
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        assert (default_title_all.title in result_data["title"]) is True
        assert self.term.shareable_link == result_data["link"]

    def test_create_social_media_content_from_object(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        emoji_1 = DjangoTestingModel.create(Emoji)
        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=social_constants.ALL,
        )

        hashtag = DjangoTestingModel.create(Hashtag, title="hashtag", platform=social_constants.TWITTER)
        result_data = content_creator(social_constants.TWITTER).create_social_media_content_from_object()
        assert default_title_all == result_data["default_title"]
        if "title_emojis" in result_data:
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        assert (default_title_all.title in result_data["title"]) is True
        assert self.term.resume == result_data["content"]
        assert self.term.shareable_link == result_data["link"]
        assert self.term == result_data["content_shared"]
        assert self.term.image == result_data["media"]
        assert TermSharedHistorial == result_data["shared_model_historial"]
        if "hashtags" in result_data:
            assert (hashtag in result_data["hashtags_list"]) is True
            assert f"#{hashtag.title}" == result_data["hashtags"]

    def test_create_random_title(self):
        content_creator = ContentCreation
        content_creator.model_class = Term
        emoji_1 = DjangoTestingModel.create(Emoji)
        default_title = DjangoTestingModel.create(DefaultTilte, title="Default title")
        result_data = content_creator().create_random_title()
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
            DefaultTilte, title="Default title news", for_content=social_constants.NEWS
        )
        result_data = content_creator().create_random_title(
            **{"default_title_filter": {"for_content": social_constants.NEWS}},
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

        result_data = content_creator().create_random_title(**{"title": "Custom title"})
        if "title_emojis" in result_data:
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        if "default_title" in result_data:
            assert default_title_news == result_data["default_title"]
        else:
            expected_data = {"title": "Custom title"}
            assert result_data == expected_data
