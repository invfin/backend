from unittest.mock import patch
from datetime import timedelta

from django.utils import timezone
from django.test import TestCase

from bfet import DjangoTestingModel

from apps.escritos.models import Term
from apps.escritos.tasks import prepare_term_newsletter_task


class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    @patch("apps.general.outils.emailing.EmailingSystem.simple_email")
    @patch("apps.escritos.tasks.notify_term_to_improve_task.delay")
    def test_prepare_term_newsletter(self, mock_simple_email, mock_notify_term_to_improve_task):
        prepare_term_newsletter_task()
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"
        mock_simple_email.called_with(subject=subject, message=message)

        term = DjangoTestingModel.create(Term)
        prepare_term_newsletter_task()
        subject = f"{term} is ready to be sent as a newsletter"
        message = f"You need to update {term} to be ready to be sent as a newsletter {term.shareable_link}"
        mock_simple_email.called_with(subject=subject, message=message)
