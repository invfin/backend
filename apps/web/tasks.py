from django.contrib.auth import get_user_model
from django.utils import timezone

from config import celery_app

from apps.general.tasks import enviar_email_task
from apps.socialmedias.socialposter.webpy import WebsiteContentCreation

from apps.web import constants
from apps.web.models import WebsiteEmail, WebsiteEmailTrack

User = get_user_model()


@celery_app.task()
def send_website_email_task():
    for email_to_send in WebsiteEmail.objects.filter(sent = False):
        if email_to_send.date_to_send <= timezone.now():
            for user in User.objects.all():
                enviar_email_task.delay(email_to_send.dict_for_task, user.id, 'web')
            email_to_send.sent = True
            email_to_send.save(update_fields=['sent'])


@celery_app.task()
def send_website_email_engagement():
    for user in User.objects.all():
        last_email_engagement = WebsiteEmailTrack.objects.filter(
            sent_to=user,
            email_related__sent=True,
            email_related__type_related__slug__startswith=constants.EMAIL_WEB_ENGAGEMENT
            )
        if (
            user.last_time_seen and
            (user.last_time_seen - last_email_engagement.date_to_send).days > 30
        ):
            email_to_send = WebsiteContentCreation.create_save_email(constants.CONTENT_FOR_ENGAGEMENT_USER_LITTLE_ACTIVE)
        elif not user.last_time_seen:
            email_to_send = WebsiteContentCreation.create_save_email(constants.CONTENT_FOR_ENGAGEMENT_USER_NO_ACTIVE)

        enviar_email_task.delay(email_to_send.dict_for_task, user.id, 'web')