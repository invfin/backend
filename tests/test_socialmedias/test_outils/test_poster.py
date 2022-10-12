import vcr

from unittest.mock import patch

from bfet import DjangoTestingModel

from django.contrib.auth import get_user_model
from django.conf import settings
from django.test import TestCase

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.public_blog.models import PublicBlog
from apps.preguntas_respuestas.models import Question
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.outils.poster import SocialPosting
from apps.socialmedias import constants

FULL_DOMAIN = settings.FULL_DOMAIN

poster_vcr = vcr.VCR(
    cassette_library_dir="cassettes/poster/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


class TestSocialPosting(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.clean_company = DjangoTestingModel.create(
            Company,
            name="Apple",
            ticker="AAPL",
            no_incs=False,
            no_bs=False,
            no_cfs=False,
            description_translated=True,
            has_logo=True,
            has_error=False,
        )
        user = DjangoTestingModel.create(get_user_model())
        cls.term = DjangoTestingModel.create(Term, title="term title", resume="term resume")
        cls.blog = DjangoTestingModel.create(PublicBlog, author=user)
        cls.question = DjangoTestingModel.create(Question, author=user)

    def test_create_link(self):
        assert "http://example.com:8000/screener/analisis-de/AAPL/" == SocialPosting().create_link(self.clean_company)

    @poster_vcr.use_cassette(filter_query_parameters=["token"])
    @patch("apps.translate.google_trans_new.google_translator.translate")
    def test_news_content(self, translated_data):
        translated_data.return_value = "noticia traducida"
        news_content = SocialPosting().news_content(self.clean_company)
        assert news_content == {
            "title": "noticia traducida",
            "description": "noticia traducida",
            "link": "http://example.com:8000/screener/analisis-de/AAPL/",
            "company_related": self.clean_company,
            "shared_model_historial": NewsSharedHistorial,
        }

    def test_company_content(self):
        with vcr.use_cassette("cassettes/company/retrieve/test_get_current_price.yaml"):
            company_poster = SocialPosting().company_content(self.clean_company)
        assert company_poster == {
            "title": "Apple",
            "description": f"{self.clean_company.short_introduction} {self.clean_company.description}",
            "link": "http://example.com:8000/screener/analisis-de/AAPL/",
            "content_shared": self.clean_company,
            "shared_model_historial": CompanySharedHistorial,
        }

    def test_question_content(self):
        term_poster = SocialPosting().question_content(self.question)
        assert term_poster == {
            "title": self.question.title,
            "description": self.question.description,
            "link": FULL_DOMAIN + self.question.get_absolute_url(),
            "content_shared": self.question,
            "shared_model_historial": QuestionSharedHistorial,
        }

    def test_term_content(self):
        term_poster = SocialPosting().term_content(self.term)
        assert term_poster == {
            "title": self.term.title,
            "description": self.term.resume,
            "link": FULL_DOMAIN + self.term.get_absolute_url(),
            "content_shared": self.term,
            "shared_model_historial": TermSharedHistorial,
        }

    def test_publicblog_content(self):
        term_poster = SocialPosting().publicblog_content(self.blog)
        assert term_poster == {
            "title": self.blog.title,
            "description": self.blog.resume,
            "link": self.blog.custom_url,
            "content_shared": self.blog,
            "shared_model_historial": BlogSharedHistorial,
        }

    # @poster_vcr.use_cassette(filter_post_data_parameters=["access_token"])
    # def test_posting_specific_term_on_facebook(self):
    #     SocialPosting().share_content(
    #         constants.TERM,
    #         [
    #             {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
    #         ],
    #         self.escrito.term,
    #     )

    # @poster_vcr.use_cassette(filter_post_data_parameters=["access_token"])
    # def test_posting_specific_term_no_resume_on_facebook(self):
    #     SocialPosting().share_content(
    #         constants.TERM,
    #         [
    #             {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
    #         ],
    #         self.escrito.empty_term,
    #     )

    # def test_clean_description(self):
    #     title, link, description = SocialPosting(QuestionSharedHistorial, self.question).generate_content()
    #     description = strip_tags(description)
    #     assert description == 'masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds sdfjhfb  fusd fvgsvd fsvd '
