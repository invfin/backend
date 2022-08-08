from django.contrib.auth import get_user_model
from django.utils import timezone

from config import celery_app
from celery import shared_task

from apps.general.tasks import send_email_task
from apps.general.constants import EMAIL_FOR_WEB
from apps.web.outils.content_creation import WebsiteContentCreation

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


#@celery_app.task()


 #       send_email_task.delay(email_to_send.dict_for_task, user.id, EMAIL_FOR_WEB, web_objective)
