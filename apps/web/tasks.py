from django.contrib.auth import get_user_model
from django.utils import timezone

from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB
from apps.general.outils.emailing import EmailingSystem
from apps.escritos.models import Term
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail


User = get_user_model()


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_email_engagement_task(email_id: int):
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
def prepare_term_newsletter():
    terms_for_newsletter = Term.objects.term_ready_newsletter()
    if terms_for_newsletter:
        subject = f"{terms_for_newsletter} is ready to be sent as a newsletter"
        message = (
            f"You need to update {terms_for_newsletter} to be ready to be sent as a newsletter"
            f" {terms_for_newsletter.shareable_link}"
        )
    else:
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"

    return EmailingSystem.simple_email(subject, message)


@shared_task(autoretry_for=(Exception,), max_retries=3)
def send_periodically_email_engagement_task():
    email_to_send = WebsiteEmail.objects.filter(sent=False, date_to_send__isnull=False).first()
    if email_to_send:
        if email_to_send.date_to_send <= timezone.now():
            return send_email_engagement_task.delay(email_to_send.id)
        return None
    return EmailingSystem.simple_email("There are no website emails ready", "Create newsletters")
