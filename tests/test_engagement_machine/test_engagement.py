from django.test import TestCase

from bfet import DjangoTestingModel

from src.content_creation import constants as content_creation_constants
from src.content_creation.models import DefaultTilte, Emoji
from src.content_creation.outils.content_creator import (
    CompanyContentCreation,
    CompanyNewsContentCreation,
    PublicBlogContentCreation,
    QuestionContentCreation,
    TermContentCreation,
)
from src.engagement_machine.outils.engagement import EngagementMachine
from src.escritos.models import Term
from src.web import constants
from src.web.models import WebsiteEmail


class TestEngagementMachine(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.defualt_title = DjangoTestingModel.create(
            DefaultTilte,
            title="Default title",
            for_content=content_creation_constants.WEB,
        )
        cls.title_emojis = DjangoTestingModel.create(Emoji, emoji="emoji")
        cls.term = DjangoTestingModel.create(Term, title="term default")

    def test_get_creator(self):
        assert (
            EngagementMachine().get_creator(content_creation_constants.QUESTION_FOR_CONTENT)
            == QuestionContentCreation
        )
        assert (
            EngagementMachine().get_creator(content_creation_constants.NEWS_FOR_CONTENT)
            == CompanyNewsContentCreation
        )
        assert (
            EngagementMachine().get_creator(content_creation_constants.TERM_FOR_CONTENT)
            == TermContentCreation
        )
        assert (
            EngagementMachine().get_creator(content_creation_constants.PUBLIC_BLOG_FOR_CONTENT)
            == PublicBlogContentCreation
        )
        assert (
            EngagementMachine().get_creator(content_creation_constants.COMPANY_FOR_CONTENT)
            == CompanyContentCreation
        )

    def test_send_website_email_engagement(self):
        title = "Default title"
        content = "Insider content"
        whom_to_send = constants.EMAIL_ALL
        newsletter_data = {
            "title": title,
            "content": content,
            "title_emojis": [self.title_emojis],
            "content": content,
            "whom_to_send": whom_to_send,
        }
        result_data = EngagementMachine().save_newsletter(**newsletter_data)
        assert isinstance(result_data, WebsiteEmail)
        assert title == result_data.title
        assert content == result_data.content
        assert (self.title_emojis in result_data.title_emojis.all()) is True
        assert whom_to_send == result_data.whom_to_send

    def test_create_newsletter(self):
        web_email_type = constants.CONTENT_FOR_ENGAGEMENT
        content_object = content_creation_constants.TERM_FOR_CONTENT
        whom_to_send = constants.EMAIL_ALL

        self.term.checkings.update({"has_information_clean": {"state": "yes", "time": ""}})
        self.term.save(update_fields=["checkings"])

        web_email = EngagementMachine().create_newsletter(
            web_email_type, content_object, whom_to_send
        )
        assert isinstance(web_email, WebsiteEmail)
