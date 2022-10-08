from django.contrib.auth import get_user_model
from django.utils import timezone

from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB

from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail

User = get_user_model()


def send_email_engagement(email: WebsiteEmail):
    if email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_ALL:
        users_to_send_to = User.objects.all()
    elif email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_TYPE_RELATED:
        users_to_send_to = email.type_related.all()
    elif email.whom_to_send == web_constants.WHOM_TO_SEND_EMAIL_SELECTED:
        users_to_send_to = email.users_selected.all()

    for user in users_to_send_to:
        send_email_task.delay(email.dict_for_task, user.id, EMAIL_FOR_WEB)
        email.sent = True
        email.save(update_fields=["sent"])


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_periodically_email_engagement_task():
    for email_to_send in WebsiteEmail.objects.filter(sent=False):
        if email_to_send.date_to_send <= timezone.now():
            send_email_engagement(email_to_send)


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_email_engagement_task(email_id: int = None):
    send_email_engagement(WebsiteEmail.objects.get(pk=email_id))
