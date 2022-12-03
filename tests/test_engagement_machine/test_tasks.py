from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from bfet import DjangoTestingModel

from src.emailing.constants import EMAIL_FOR_WEB
from src.engagement_machine.tasks import check_and_start_send_email_engagement_task, send_email_engagement_task
from src.promotions.models import Campaign
from src.users.models import User, UsersCategory
from src.web import constants as web_constants
from src.web.models import WebsiteEmail


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    @patch("src.engagement_machine.tasks.send_email_engagement_task.delay")
    @patch("src.emailing.outils.emailing.EmailingSystem.simple_email")
    def test_check_and_start_send_email_engagement_task(self, mock_send_email_engagement_task, mock_simple_email):
        check_and_start_send_email_engagement_task()
        mock_simple_email.called_with("There are no website emails ready", "Create newsletters")

        yesterday = timezone.now() - timedelta(days=1)
        web_newsletter_yesterday = DjangoTestingModel.create(WebsiteEmail, sent=False, date_to_send=yesterday)
        check_and_start_send_email_engagement_task()
        mock_send_email_engagement_task.called_with(web_newsletter_yesterday.id)
        web_newsletter_yesterday.sent = True
        web_newsletter_yesterday.save(update_fields=["sent"])

        tomorrow = timezone.now() + timedelta(days=1)
        DjangoTestingModel.create(WebsiteEmail, sent=False, date_to_send=tomorrow)
        assert check_and_start_send_email_engagement_task() is None

    @patch("src.emailing.tasks.send_email_task.delay")
    def test_send_email_engagement_task(self, mock_send_email_task):
        with self.subTest(web_constants.WHOM_TO_SEND_EMAIL_CAMPAIGN_RELATED):
            users_category = DjangoTestingModel.create(UsersCategory)
            user_1 = DjangoTestingModel.create(User)
            users_category.users.add(user_1)
            campaign = DjangoTestingModel.create(Campaign, users_category=users_category)

            email_with_campaign = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.WHOM_TO_SEND_EMAIL_CAMPAIGN_RELATED,
            )

            send_email_engagement_task(email_with_campaign.id)
            # mock_send_email_task.call_count
            mock_send_email_task.has_been_called_with(
                email_with_campaign.dict_for_task,
                user_1.id,
                EMAIL_FOR_WEB,
            )
            email_with_campaign.refresh_from_db()
            assert email_with_campaign.sent is True

        with self.subTest(web_constants.WHOM_TO_SEND_EMAIL_SELECTED):
            email_with_users = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.WHOM_TO_SEND_EMAIL_SELECTED,
            )
            user_2 = DjangoTestingModel.create(User)
            email_with_users.users_selected.add(user_2)
            send_email_engagement_task(email_with_users.id)
            mock_send_email_task.has_been_called_with(
                email_with_users.dict_for_task,
                user_2.id,
                EMAIL_FOR_WEB,
            )
            email_with_users.refresh_from_db()
            assert email_with_users.sent is True

        with self.subTest(web_constants.WHOM_TO_SEND_EMAIL_ALL):
            email_with_all = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.WHOM_TO_SEND_EMAIL_ALL,
            )
            send_email_engagement_task(email_with_all.id)
            mock_send_email_task.has_been_called_with(
                email_with_all.dict_for_task,
                user_1.id,
                EMAIL_FOR_WEB,
            )
            mock_send_email_task.has_been_called_with(
                email_with_all.dict_for_task,
                user_2.id,
                EMAIL_FOR_WEB,
            )
            email_with_all.refresh_from_db()
            assert email_with_all.sent is True
