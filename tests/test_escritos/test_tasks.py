from unittest.mock import patch

from django.test import TestCase

from bfet import DjangoTestingModel

from src.escritos.models import Term
from src.escritos.tasks import prepare_term_newsletter_task
from src.socialmedias.models import DefaultTilte

class TestTask(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        pass

    @patch("src.emailing.outils.emailing.EmailingSystem.simple_email")
    @patch("src.escritos.tasks.notify_term_to_improve_task.delay")
    def test_prepare_term_newsletter(self, mock_simple_email, mock_notify_term_to_improve_task):
        DjangoTestingModel.create(DefaultTilte, title="title", for_content=6, purpose="Engagement user no active")
        DjangoTestingModel.create(DefaultTilte, title="title", for_content=0, purpose="Engagement user no active")
        prepare_term_newsletter_task()
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"
        mock_simple_email.called_with(subject=subject, message=message)

        term = DjangoTestingModel.create(Term)

        prepare_term_newsletter_task()
        subject = f"{term} is ready to be sent as a newsletter"
        message = f"You need to update {term} to be ready to be sent as a newsletter {term.shareable_link}"
        mock_simple_email.called_with(subject=subject, message=message)
