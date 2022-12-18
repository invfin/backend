from typing import Dict, Optional, Tuple

from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet
from django.utils import timezone

from celery import shared_task

from src.emailing.constants import EMAIL_FOR_WEB
from src.emailing.outils.emailing import EmailingSystem
from src.emailing.tasks import send_email_task
from src.web import constants as web_constants
from src.web.models import WebsiteEmail

User = get_user_model()


class EmailEngamentTask:
    email: WebsiteEmail

    def __init__(self, email_id: int) -> None:
        self.email = self.get_email(email_id)

    @staticmethod
    def get_email(email_id: int) -> WebsiteEmail:
        return WebsiteEmail.objects.get(pk=email_id)

    def email_is_for_campaign(self) -> bool:
        return self.email.whom_to_send == web_constants.EMAIL_CAMPAIGN_RELATED

    def return_manager_for_campaign_email(self) -> Optional[type]:
        if self.email_is_for_campaign():
            return self.email.campaign.users_category.users
        return None

    def get_users_to_email_queryset(self) -> QuerySet:
        users_managers_possibilities = {
            web_constants.EMAIL_CAMPAIGN_RELATED: self.return_manager_for_campaign_email(),
            web_constants.EMAIL_SELECTED: self.email.users_selected,
            web_constants.EMAIL_ALL: User.objects,
        }
        users_manager = users_managers_possibilities[self.email.whom_to_send]
        print(users_manager.exclude(Q(for_testing=True) | Q(is_bot=True)))
        return users_manager.exclude(Q(for_testing=True) | Q(is_bot=True))

    def get_email_parameters_to_send(self) -> Tuple[Dict, str]:
        email_serialized = {"sender": "InvFin", **self.email.email_serialized}
        web_objective = self.email.campaign.slug
        return email_serialized, web_objective

    def set_email_as_sent(self) -> None:
        self.email.sent = True
        self.email.save(update_fields=["sent"])
        return None

    def return_emailing_info(self) -> Tuple[QuerySet, Dict, str]:
        users_to_email = self.get_users_to_email_queryset()
        email_serialized, web_objective = self.get_email_parameters_to_send()
        return users_to_email, email_serialized, web_objective

    def send_email_engagement(self) -> None:
        users_to_email, email_serialized, web_objective = self.return_emailing_info()
        for user in users_to_email:
            send_email_task.delay(email_serialized, user.id, EMAIL_FOR_WEB, web_objective)
        return None

    def perform_emailg_and_save(self) -> None:
        self.send_email_engagement()
        self.set_email_as_sent()
        return None

    @staticmethod
    def find_email_to_send() -> Optional[WebsiteEmail]:
        return (
            WebsiteEmail.objects.filter(
                sent=False,
                date_to_send__isnull=False,
            )
            .order_by("date_to_send")
            .first()
        )

    @staticmethod
    def is_email_available_to_send(email_to_send: Optional[WebsiteEmail]) -> bool:
        # TODO test
        return email_to_send is not None and email_to_send.date_to_send <= timezone.now()

    @classmethod
    def send_email_waiting(cls) -> Optional[WebsiteEmail]:
        # TODO test
        email_to_send = cls.find_email_to_send()
        return email_to_send if cls.is_email_available_to_send(email_to_send) else None


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_email_engagement_task(email_id: int):
    """
    Receives an email id for the web. And it sends it to the users related.
    Then it checks the email as sent
    TODO: Change and generalise this tasks to send emails periodically
    """
    EmailEngamentTask(email_id).perform_emailg_and_save()


@shared_task(autoretry_for=(Exception,), max_retries=3)
def check_and_start_send_email_engagement_task():
    """From all the emails from the website filter wich have a date to send, that means that they are ready
    to be sent.

    Returns
    -------
        None
            If there is any email ready to be sent, it sends it, otherwise it waits if the email's time to send isn't
            the moment it return None. Finally if there isn't any email ready it sends an email.
            Example:
    """
    email_to_send = EmailEngamentTask.send_email_waiting()
    if email_to_send:
        send_email_engagement_task.delay(email_to_send.id)
        return EmailingSystem.simple_email(
            f"Newsletter {email_to_send.id} sent",
            f"Newsletter with the object {email_to_send.object} has been sent",
        )
    return None
