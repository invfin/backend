import vcr

from unittest.mock import patch

from bfet import DjangoTestingModel

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase

from apps.empresas.models import Company, IncomeStatement
from apps.escritos.models import Term
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.preguntas_respuestas.models import Question
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter
from apps.socialmedias.outils.content_creation import (
    CompanyContentCreation,
    CompanyNewsContentCreation,
    TermContentCreation,
    QuestionContentCreation,
    PublicBlogContentCreation,
)
from apps.socialmedias.outils.poster import SocialPosting
from apps.socialmedias import constants
from apps.socialmedias.models import Emoji, DefaultTilte

FULL_DOMAIN = settings.FULL_DOMAIN

poster_vcr = vcr.VCR(
    cassette_library_dir="cassettes/poster/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


class TestSocialPosting(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.clean_company = DjangoTestingModel.create(
            Company, name="Apple", ticker="AAPL", description="long ass description"
        )
        DjangoTestingModel.create(IncomeStatement, company=cls.clean_company)
        user = DjangoTestingModel.create(get_user_model(), username="lucas")
        writter_profile = DjangoTestingModel.create(
            WritterProfile, user=user, host_name="lucas", long_description="long ass description for writter"
        )
        cls.term = DjangoTestingModel.create(Term, title="term title", resume="term resume")
        cls.blog = DjangoTestingModel.create(PublicBlog, title="blog title", resume="blog resume", author=user)
        cls.question = DjangoTestingModel.create(Question, title="question title", author=user)
        cls.fb_emoji = DjangoTestingModel.create(Emoji)
        cls.default_title = DjangoTestingModel.create(DefaultTilte, title="Default title", for_content=constants.ALL)

    def test_get_creator(self):
        for content, content_creator in [
            (constants.QUESTION_FOR_CONTENT, QuestionContentCreation),
            (constants.NEWS_FOR_CONTENT, CompanyNewsContentCreation),
            (constants.TERM_FOR_CONTENT, TermContentCreation),
            (constants.PUBLIC_BLOG_FOR_CONTENT, PublicBlogContentCreation),
            (constants.COMPANY_FOR_CONTENT, CompanyContentCreation),
        ]:
            with self.subTest(content):
                assert content_creator == SocialPosting().get_creator(content)

    def test_get_socialmedia(self):
        assert isinstance(SocialPosting().get_socialmedia(constants.FACEBOOK), Facebook)
        assert isinstance(SocialPosting().get_socialmedia(constants.TWITTER), Twitter)

    @patch("apps.socialmedias.socialposter.facepy.Facebook.post")
    @patch("apps.socialmedias.socialposter.tweetpy.Twitter.post")
    def test_share_content(self, mock_facepy, mock_tweetpy):
        SocialPosting().share_content(
            constants.TERM_FOR_CONTENT,
            [
                {"platform_shared": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT_IMAGE},
                {"platform_shared": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT_IMAGE},
            ],
        )
        mock_facepy.return_value = {
            "post_response": [
                {
                    "social_id": "64dsf8g4dfg45dfh",
                    "title": title,
                    "content": "face content",
                    "post_type": constants.POST_TYPE_TEXT_IMAGE,
                    "use_hashtags": True,
                    "use_emojis": True,
                    "use_link": True,
                    "use_default_title": True,
                    "use_default_content": True,
                }
            ]
        }
        mock_tweetpy.return_value = {
            "post_response": [
                {
                    "social_id": "1dfg1661dh4fg",
                    "content": title,
                    "post_type": constants.POST_TYPE_TEXT_IMAGE,
                    "use_hashtags": False,
                    "use_emojis": True,
                    "use_link": False,
                    "use_default_title": True,
                    "use_default_content": False,
                },
                {
                    "social_id": "dg5h71fghfgh",
                    "content": last_tweet,
                    "post_type": constants.POST_TYPE_THREAD,
                    "use_hashtags": True,
                    "use_link": True,
                    "use_emojis": False,
                    "use_default_title": False,
                    "use_default_content": False,
                },
            ]
        }

    def test_prepare_data_to_be_saved(self):
        socialmedia_content = {
            "default_title": self.default_title,
            "title": "term title Default title",
            "content": (
                f"{self.term.resume} <br>Si quieres conocer más a fondo puedes leer la definición entera"
                f" http://example.com:8000/{self.term.slug}. <br>Estos son los puntos claves que encontrarás:"
            ),
            f"link": "http://example.com:8000/{self.term.slug}",
            "content_shared": self.term,
            "media": self.term.image,
            "shared_model_historial": TermSharedHistorial,
            "hashtags_list": [],
            "hashtags": "",
        }
        SocialPosting().prepare_data_to_be_saved(
            # socialmedia_post_response,
            # platform_shared,
            # link,
            socialmedia_content,
        )

    def test_save_content_posted(self):
        pass
