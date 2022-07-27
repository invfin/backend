from django.contrib.auth import get_user_model
from django.utils import timezone

from apps.general.tasks import enviar_email_task
from config import celery_app

from . import constants
from .models import WebsiteEmail, WebsiteEmailTrack

User = get_user_model()


@celery_app.task()
def send_website_email_task():
    for email_to_send in WebsiteEmail.objects.filter(sent = False):
        if email_to_send.date_to_send <= timezone.now():
            for user in User.objects.all():
                enviar_email_task.delay(email_to_send.for_task, user.id, 'web')
            email_to_send.sent = True
            email_to_send.save()


@celery_app.task()
def send_website_email_engagement():
    for user in User.objects.all():
        last_email_engagement = WebsiteEmailTrack.objects.filter(
            sent_to=user,
            email_related__sent=True,
            email_related__type_related__slug=constants.EMAIL_WEB_ENGAGEMENT
            )
        if (
            user.last_time_seen and
            (user.last_time_seen - last_email_engagement.date_to_send).days > 30
        ):
            pass
        elif not user.last_time_seen:
            pass