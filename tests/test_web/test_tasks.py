from unittest.mock import patch
from datetime import timedelta

from django.core import mail
from django.utils import timezone
from django.test import TestCase

from bfet import DjangoTestingModel

from apps.general.constants import EMAIL_FOR_WEB
from apps.escritos.models import Term
from apps.users.models import User
from apps.web.tasks import prepare_term_newsletter, send_periodically_email_engagement_task, send_email_engagement_task
from apps.web.models import WebsiteEmail, WebsiteEmailsType, UserAndVisiteurCategory
from apps.web import constants as web_constants


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    @patch("apps.general.outils.emailing.EmailingSystem.simple_email")
    def test_prepare_term_newsletter(self, mock_simple_email):
        prepare_term_newsletter()
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"
        mock_simple_email.called_with(subject=subject, message=message)

        term = DjangoTestingModel.create(Term)
        prepare_term_newsletter()
        subject = f"{term} is ready to be sent as a newsletter"
        message = (
            f"You need to update {term} to be ready to be sent as a newsletter"
            f" {term.shareable_link}"
        )
        mock_simple_email.called_with(subject=subject, message=message)

    @patch("apps.web.tasks.send_email_engagement_task")
    @patch("apps.general.outils.emailing.EmailingSystem.simple_email")
    def test_send_periodically_email_engagement_task(self, mock_send_email_engagement_task, mock_simple_email):
        send_periodically_email_engagement_task()
        mock_simple_email.called_with("There are no website emails ready", "Create newsletters")

        yesterday = timezone.now() - timedelta(days=1)
        web_newsletter_yesterday = DjangoTestingModel.create(WebsiteEmail, sent=False, date_to_send=yesterday)
        send_periodically_email_engagement_task()
        mock_send_email_engagement_task.called_with(web_newsletter_yesterday.id)
        web_newsletter_yesterday.sent = True
        web_newsletter_yesterday.save(update_fields=["sent"])

        tomorrow = timezone.now() + timedelta(days=1)
        DjangoTestingModel.create(WebsiteEmail, sent=False, date_to_send=tomorrow)
        assert send_periodically_email_engagement_task() is None

    @patch("apps.general.tasks.send_email_task")
    def test_send_email_engagement_task(self, mock_send_email_task):
        email_type = DjangoTestingModel.create(WebsiteEmailsType)
        email = DjangoTestingModel.create(WebsiteEmail, type_related=email_type)
        users_category = DjangoTestingModel.create(UserAndVisiteurCategory)
        user_1 = DjangoTestingModel.create(User)
        user_2 = DjangoTestingModel.create(User)
        users_category.users.add(user_1)
        users_category.email_type_related.add(email_type)
        email.users_selected.add(user_2)

        email.whom_to_send = web_constants.WHOM_TO_SEND_EMAIL_TYPE_RELATED
        email.save(update_fields=["whom_to_send"])
        send_email_engagement_task(email.id)
        mock_send_email_task.called_with(email.dict_for_task, user_1.id, EMAIL_FOR_WEB)
        assert email.sent is True
        assert len(mail.outbox) == 1

        email.whom_to_send = web_constants.WHOM_TO_SEND_EMAIL_SELECTED
        email.sent = False
        email.save(update_fields=["whom_to_send", "sent"])
        send_email_engagement_task(email.id)
        mock_send_email_task.called_with(email.dict_for_task, user_2.id, EMAIL_FOR_WEB)
        assert email.sent is True
        assert len(mail.outbox) == 1

        email.whom_to_send = web_constants.WHOM_TO_SEND_EMAIL_ALL
        email.sent = False
        email.save(update_fields=["whom_to_send", "sent"])
        send_email_engagement_task(email.id)
        mock_send_email_task.called_with(email.dict_for_task, user_1.id, EMAIL_FOR_WEB)
        mock_send_email_task.called_with(email.dict_for_task, user_2.id, EMAIL_FOR_WEB)
        assert email.sent is True

        sent_email = mail.outbox[0]
        assert len(mail.outbox) == 2

