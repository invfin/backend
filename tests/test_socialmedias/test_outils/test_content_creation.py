import vcr

from unittest.mock import patch

from bfet import DjangoTestingModel

from django.test import TestCase
from django.contrib.auth import get_user_model

from apps.socialmedias.outils.content_creation import ContentCreation
from apps.socialmedias import constants as social_constants
from apps.web import constants as web_constants
from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.public_blog.models import PublicBlog, WritterProfile
from apps.preguntas_respuestas.models import Question
from apps.

class TestContentCreation(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.clean_company = DjangoTestingModel.create(
            Company, name="Apple", ticker="AAPL", description="long ass description"
        )
        user = DjangoTestingModel.create(get_user_model(), username="lucas")
        writter_profile = DjangoTestingModel.create(WritterProfile, user=user, host_name="lucas", long_description="long ass description for writter")
        cls.term = DjangoTestingModel.create(Term, title="term title", resume="term resume")
        cls.blog = DjangoTestingModel.create(PublicBlog, title="blog title", resume="blog resume", author=user)
        cls.question = DjangoTestingModel.create(Question, title="question title", author=user)

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
