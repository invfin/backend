from typing import Type

from bfet import DjangoTestingModel

from src.content_creation import constants
from src.content_creation.models import DefaultTilte, Emoji, Hashtag
from src.content_creation.outils.content_creator import ContentCreation
from src.escritos.models import Term
from src.socialmedias import constants as social_constants
from src.socialmedias.models import TermSharedHistorial


class BaseTestContentCreation:
    # TODO patch the random generated contents
    content_creator: Type = None
    model_class: Type = None
    shared_model_historial: Type = None
    model_class_obj: Type = None

    def setUp(self) -> None:
        self.content_creator = self.content_creator
        self.model_class = self.model_class
        self.shared_model_historial = self.shared_model_historial
        self.model_class_obj = self.model_class_obj

    def test_get_object(self):
        assert self.content_creator().get_object() == self.model_class_obj

    def test_get_shared_model_historial(self):
        assert (
            self.content_creator().get_shared_model_historial() == self.shared_model_historial
        )

    def test_get_object_title(self):
        assert self.model_class_obj.title == self.content_creator().get_object_title()

    def test_get_object_content(self):
        assert self.model_class_obj.resume == self.content_creator().get_object_content()

    def test_get_object_media(self):
        assert self.model_class_obj.image == self.content_creator().get_object_media()

    def test_create_url(self):
        assert self.content_creator().create_url() == self.model_class_obj.shareable_link

    def test_prepare_inital_data(self):
        emoji_1 = DjangoTestingModel.create(Emoji)

        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=constants.ALL,
        )
        result_data = self.content_creator().prepare_inital_data()
        assert default_title_all == result_data["default_title"]
        assert self.model_class_obj.resume == result_data["content"]
        assert self.model_class_obj == result_data["content_shared"]
        if "title_emojis" in result_data:
            # Emoji might or might not be here because it's randomly generated
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        assert (default_title_all.title in result_data["title"]) is True
        assert self.model_class_obj.shareable_link == result_data["link"]

    def test_create_newsletter_content_from_object(self):
        emoji_1 = DjangoTestingModel.create(Emoji)

        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=constants.ALL,
        )
        result_data = self.content_creator().create_newsletter_content_from_object()
        assert default_title_all == result_data["default_title"]
        assert self.model_class_obj.resume == result_data["content"]
        assert self.model_class_obj == result_data["content_shared"]
        if "title_emojis" in result_data:
            # Emoji might or might not be here because it's randomly generated
            assert (emoji_1 in result_data["title_emojis"]) is True
            assert (emoji_1.emoji in result_data["title"]) is True
        assert (default_title_all.title in result_data["title"]) is True
        assert self.model_class_obj.shareable_link == result_data["link"]

    def test_create_social_media_content_from_object(self):
        emoji_1 = DjangoTestingModel.create(Emoji)
        default_title_all = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=constants.ALL,
        )
        for socialmedia in social_constants.SOCIAL_MEDIAS_USED:
            with self.subTest(socialmedia):
                hashtag = DjangoTestingModel.create(
                    Hashtag, title="hashtag", platform=socialmedia
                )
                result_data = self.content_creator(
                    socialmedia
                ).create_social_media_content_from_object()
                assert default_title_all == result_data["default_title"]
                if "title_emojis" in result_data:
                    assert (emoji_1 in result_data["title_emojis"]) is True
                    assert (emoji_1.emoji in result_data["title"]) is True
                assert (default_title_all.title in result_data["title"]) is True
                assert self.model_class_obj.resume == result_data["content"]
                assert self.model_class_obj.shareable_link == result_data["link"]
                assert self.model_class_obj == result_data["content_shared"]
                assert self.model_class_obj.image == result_data["media"]
                assert TermSharedHistorial == result_data["shared_model_historial"]
                if "hashtags" in result_data:
                    assert (hashtag in result_data["hashtags_list"]) is True
                    assert f"#{hashtag.title}" == result_data["hashtags"]

    def test_create_default_title_filter(self):
        with self.subTest("content All"):
            content_creator_all = ContentCreation
            content_creator_all.model_class = Term
            content_creator_all.for_content = []
            assert content_creator_all().create_default_title_filter() == {
                "for_content__in": [constants.ALL]
            }
        with self.subTest("content with Web"):
            content_creator_web = ContentCreation
            content_creator_web.model_class = Term
            content_creator_web.for_content = []
            assert content_creator_web(
                constants.PLATFORM_WEB
            ).create_default_title_filter() == {
                "for_content__in": [constants.ALL, constants.WEB]
            }

    def test_create_default_content_filter(self):
        with self.subTest("content All"):
            content_creator_all = ContentCreation
            content_creator_all.model_class = self.model_class
            content_creator_all.for_content = []
            assert content_creator_all().create_default_title_filter() == {
                "for_content__in": [constants.ALL]
            }
        with self.subTest("content with Web"):
            content_creator_web = ContentCreation
            content_creator_web.model_class = self.model_class
            content_creator_web.for_content = []
            assert content_creator_web(
                constants.PLATFORM_WEB
            ).create_default_title_filter() == {
                "for_content__in": [constants.ALL, constants.WEB]
            }
