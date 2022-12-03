from typing import Dict

from config import celery_app

from src.emailing.outils.emailing import EmailingSystem
from src.notifications.outils.notifications import NotificationSystem


@celery_app.task()
def send_email_task(email: Dict, receiver_id: int, is_for: str = "", web_objective: str = ""):
    return EmailingSystem(is_for, web_objective).enviar_email(email, receiver_id)


@celery_app.task()
def prepare_notification_task(object_related: Dict, notif_type: str):
    notification_info = NotificationSystem().notify(object_related, notif_type)
    for notif in notification_info:
        send_email_task.delay(**notif)
