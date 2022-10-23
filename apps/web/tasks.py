from django.contrib.auth import get_user_model
from django.utils import timezone

from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB
from apps.general.outils.emailing import EmailingSystem
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail

User = get_user_model()


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_email_engagement_task(email_id: int):
    """Recieves an email id for the web. And it sends it to the users related.
    Then it checks the email as sent

    Parameters
    ----------
        email_id : int
            The id of the email
    """
    email = WebsiteEmail.objects.get(pk=email_id)
    if email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_ALL:
        users_to_send_to = User.objects.all()
    elif email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_TYPE_RELATED:
        users_to_send_to = email.type_related.users_categories.all()
    elif email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_SELECTED:
        users_to_send_to = email.users_selected.all()

    for user in users_to_send_to:
        send_email_task.delay(email.dict_for_task, user.id, EMAIL_FOR_WEB)
    email.sent = True
    email.save(update_fields=["sent"])


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
    email_to_send = WebsiteEmail.objects.filter(sent=False, date_to_send__isnull=False).first()
    if email_to_send:
        if email_to_send.date_to_send <= timezone.now():
            send_email_engagement_task.delay(email_to_send.id)
            return EmailingSystem.simple_email(
                f"Newsletter sent {email_to_send.id}",
                f"Newsletter with the object {email_to_send.object} has been sent",
            )
        return None
    return EmailingSystem.simple_email("There are no website emails ready", "Create newsletters")
