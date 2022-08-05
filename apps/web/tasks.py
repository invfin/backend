from django.contrib.auth import get_user_model
from django.utils import timezone

from config import celery_app
from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB
from apps.socialmedias.socialposter.webpy import WebsiteContentCreation

from apps.web import constants
from apps.web.models import WebsiteEmail, WebsiteEmailTrack
from .utils import more_than_month
User = get_user_model()

# @shared_task(autoretry_for=(Exception,), max_retries=3)
@celery_app.task()
def send_website_email_task():
    for email_to_send in WebsiteEmail.objects.filter(sent = False):
        if email_to_send.date_to_send <= timezone.now():
            for user in User.objects.all():
                send_email_task.delay(email_to_send.dict_for_task, user.id, 'web')
            email_to_send.sent = True
            email_to_send.save(update_fields=['sent'])


@celery_app.task()
def send_website_email_engagement():
    for user in User.objects.all():
        last_email_engagement = WebsiteEmailTrack.objects.filter(
            sent_to=user,
            email_related__sent=True,
            email_related__type_related__slug__startswith=constants.CONTENT_FOR_ENGAGEMENT
            )
        if last_email_engagement.exists():
            # If an email for engagement has already been sent then we check when was the last time the user
            # visited the web
            if (
                user.last_time_seen and
                more_than_month(user.last_time_seen, last_email_engagement.date_to_send)
                # If the user hasn't visited the web in the last month (29 days)

            ):
                web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_LITTLE_ACTIVE
            elif (
                not user.last_time_seen and
                more_than_month(last_email_engagement.date_to_send)
                # If the user has never visited the web and the last email was sent more then a month back
            ):
                web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_NO_ACTIVE
        else:
            web_objective = constants.CONTENT_FOR_ENGAGEMENT_USER_FIRST_CALL

        email_to_send = WebsiteContentCreation.create_save_email(web_objective)

        send_email_task.delay(email_to_send.dict_for_task, user.id, EMAIL_FOR_WEB, web_objective)
