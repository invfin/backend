from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB
from apps.escritos.models import Term
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail


User = get_user_model()


def send_email_engagement(email: WebsiteEmail):
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
def prepare_term_newsletter():
    terms_for_newsletter = Term.objects.term_ready_newsletter()
    return send_mail(
        f"{terms_for_newsletter} is ready to be sent as a newsletter",
        f"You need to update {terms_for_newsletter} to be ready to be sent as a newsletter"
        f" {terms_for_newsletter.shareable_link}",
        settings.EMAIL_DEFAULT,
        [settings.EMAIL_DEFAULT],
    )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_periodically_email_engagement_task():
    email_to_send = WebsiteEmail.objects.filter(sent=False, date_to_send__isnull=False).first()
    if email_to_send and email_to_send.date_to_send <= timezone.now():
        send_email_engagement(email_to_send)


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_email_engagement_task(email_id: int = None):
    send_email_engagement(WebsiteEmail.objects.get(pk=email_id))
