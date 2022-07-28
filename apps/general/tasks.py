from typing import Dict

from config import celery_app

from apps.general.outils.emailing import EmailingSystem
from apps.general.outils.notifications import NotificationSystem


@celery_app.task()
def enviar_email_task(is_for:str, email:Dict, receiver_id:int, email_type:str):
    return EmailingSystem(is_for).enviar_email(email, receiver_id, email_type)


@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().notify(object_related, notif_type)
