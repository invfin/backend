from typing import Dict

from config import celery_app

from apps.general.outils.emailing import EmailingSystem
from apps.general.outils.notifications import NotificationSystem


@celery_app.task()
def send_email_task(email:Dict, receiver_id:int, is_for:str=None, web_objective:str=None):
    return EmailingSystem(is_for, web_objective).enviar_email(email, receiver_id)


@celery_app.task()
def prepare_notifications_task(object_related, notif_type):
    return NotificationSystem().notify(object_related, notif_type)
