from datetime import datetime, timedelta
from unittest import skip
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from bfet import DjangoTestingModel, create_random_datetime

from src.emailing.constants import EMAIL_FOR_WEB
from src.engagement_machine.tasks import (
    EmailEngamentTask,
    check_and_start_send_email_engagement_task,
    send_email_engagement_task,
)
from src.promotions.models import Campaign
from src.users.models import User, UsersCategory
from src.web import constants as web_constants
from src.web.models import WebsiteEmail


class TestEmailEngamentTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user_for_all = DjangoTestingModel.create(
            User,
            is_bot=False,
            for_testing=False,
            first_name="for_all",
            last_name="na",
        )
        cls.user_for_category = DjangoTestingModel.create(
            User,
            id=987,
            is_bot=False,
            for_testing=False,
            first_name="for_category",
            last_name="na",
        )
        cls.user_selected = DjangoTestingModel.create(
            User,
            is_bot=False,
            for_testing=False,
            first_name="selected",
            last_name="na",
        )
        cls.user_bot = DjangoTestingModel.create(
            User,
            is_bot=True,
            for_testing=False,
            first_name="r",
        )
        cls.user_testing = DjangoTestingModel.create(
            User,
            username="algo45",
            is_bot=False,
            for_testing=True,
            first_name="s",
        )
        cls.email_for_all = DjangoTestingModel.create(
            WebsiteEmail,
            id=86,
            whom_to_send=web_constants.EMAIL_ALL,
            sent=False,
            date_to_send=create_random_datetime(5, 10, 2022),
        )
        users_category = DjangoTestingModel.create(UsersCategory)
        users_category.users.add(cls.user_for_category)
        campaign = DjangoTestingModel.create(
            Campaign,
            users_category=users_category,
            slug="campaign-slug",
        )
        cls.email_campaign = DjangoTestingModel.create(
            WebsiteEmail,
            id=741,
            whom_to_send=web_constants.EMAIL_CAMPAIGN_RELATED,
            sent=False,
            campaign=campaign,
            date_to_send=datetime(2020, 1, 22),
        )
        cls.email_for_selected = DjangoTestingModel.create(
            WebsiteEmail,
            id=19867,
            whom_to_send=web_constants.EMAIL_SELECTED,
            sent=False,
            date_to_send=datetime(2021, 9, 12),
        )
        cls.email_for_selected.users_selected.add(cls.user_selected)
        cls.engagement_task_all = EmailEngamentTask(86)
        cls.engagement_task_selected = EmailEngamentTask(19867)
        cls.engagement_task_campaign = EmailEngamentTask(741)

    def test_get_email(self):
        self.email_for_all == EmailEngamentTask.get_email(86)

    def test_email_is_for_campaign(self):
        assert self.engagement_task_campaign.email_is_for_campaign() is True
        assert self.engagement_task_selected.email_is_for_campaign() is False
        assert self.engagement_task_all.email_is_for_campaign() is False

    @skip("see how to test it")
    def test_return_manager_for_campaign_email(self):
        manager = self.engagement_task_campaign.return_manager_for_campaign_email()
        assert isinstance(manager, None)

    def test_get_users_to_email_queryset_all(self):
        result = self.engagement_task_all.get_users_to_email_queryset()
        self.assertIn(self.user_for_all, result)
        self.assertIn(self.user_for_category, result)
        self.assertIn(self.user_selected, result)
        self.assertNotIn(self.user_bot, result)
        self.assertNotIn(self.user_testing, result)

    def test_get_users_to_email_queryset_selected(self):
        result = self.engagement_task_selected.get_users_to_email_queryset()
        self.assertNotIn(self.user_for_all, result)
        self.assertNotIn(self.user_for_category, result)
        self.assertIn(self.user_selected, result)
        self.assertNotIn(self.user_bot, result)
        self.assertNotIn(self.user_testing, result)

    def test_get_users_to_email_queryset_campaign(self):
        result = self.engagement_task_campaign.get_users_to_email_queryset()
        self.assertNotIn(self.user_for_all, result)
        self.assertIn(self.user_for_category, result)
        self.assertNotIn(self.user_selected, result)
        self.assertNotIn(self.user_bot, result)
        self.assertNotIn(self.user_testing, result)

    def test_set_email_as_sent(self):
        email = DjangoTestingModel.create(
            WebsiteEmail,
            sent=False,
        )
        EmailEngamentTask(email.id).set_email_as_sent()
        email.refresh_from_db()
        assert email.sent is True

    def test_get_email_parameters_to_send(self):
        email_serialized, web_objective = (
            self.engagement_task_campaign.get_email_parameters_to_send()
        )
        assert "campaign-slug" == web_objective
        assert email_serialized == {"sender": "InvFin", **self.email_campaign.email_serialized}

    def test_return_emailing_info(self):
        users_to_email, email_serialized, web_objective = (
            self.engagement_task_campaign.return_emailing_info()
        )
        assert "campaign-slug" == web_objective
        assert email_serialized == {"sender": "InvFin", **self.email_campaign.email_serialized}
        self.assertNotIn(self.user_for_all, users_to_email)
        self.assertIn(self.user_for_category, users_to_email)
        self.assertNotIn(self.user_selected, users_to_email)
        self.assertNotIn(self.user_bot, users_to_email)
        self.assertNotIn(self.user_testing, users_to_email)

    @patch("src.emailing.tasks.send_email_task.delay")
    def test_send_email_engagement(self, mock_send_email_task):
        self.engagement_task_campaign.send_email_engagement()
        mock_send_email_task.assert_called_once_with(
            {"sender": "InvFin", **self.email_campaign.email_serialized},
            987,
            EMAIL_FOR_WEB,
            "campaign-slug",
        )

    @patch("src.emailing.tasks.send_email_task.delay")
    def test_perform_emailg_and_save(self, mock_send_email_task):
        self.engagement_task_campaign.perform_emailg_and_save()
        mock_send_email_task.assert_called_once_with(
            {"sender": "InvFin", **self.email_campaign.email_serialized},
            987,
            EMAIL_FOR_WEB,
            "campaign-slug",
        )
        self.email_campaign.refresh_from_db()
        assert self.email_campaign.sent is True

    def test_find_email_to_send(self):
        assert self.email_campaign == EmailEngamentTask.find_email_to_send()


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    @patch("src.engagement_machine.tasks.send_email_engagement_task.delay")
    @patch("src.emailing.outils.emailing.EmailingSystem.simple_email")
    def test_check_and_start_send_email_engagement_task(
        self, mock_send_email_engagement_task, mock_simple_email
    ):
        check_and_start_send_email_engagement_task()
        mock_simple_email.called_with(
            "There are no website emails ready", "Create newsletters"
        )

        yesterday = timezone.now() - timedelta(days=1)
        web_newsletter_yesterday = DjangoTestingModel.create(
            WebsiteEmail, sent=False, date_to_send=yesterday
        )
        check_and_start_send_email_engagement_task()
        mock_send_email_engagement_task.called_with(web_newsletter_yesterday.id)
        web_newsletter_yesterday.sent = True
        web_newsletter_yesterday.save(update_fields=["sent"])

        tomorrow = timezone.now() + timedelta(days=1)
        DjangoTestingModel.create(WebsiteEmail, sent=False, date_to_send=tomorrow)
        assert check_and_start_send_email_engagement_task() is None

    @patch("src.emailing.tasks.send_email_task.delay")
    def test_send_email_engagement_task(self, mock_send_email_task):
        with self.subTest(web_constants.EMAIL_CAMPAIGN_RELATED):
            users_category = DjangoTestingModel.create(UsersCategory)
            user_1 = DjangoTestingModel.create(User)
            users_category.users.add(user_1)
            campaign = DjangoTestingModel.create(Campaign, users_category=users_category)

            email_with_campaign = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.EMAIL_CAMPAIGN_RELATED,
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

        with self.subTest(web_constants.EMAIL_SELECTED):
            email_with_users = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.EMAIL_SELECTED,
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

        with self.subTest(web_constants.EMAIL_ALL):
            email_with_all = DjangoTestingModel.create(
                WebsiteEmail,
                sent=False,
                campaign=campaign,
                whom_to_send=web_constants.EMAIL_ALL,
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
