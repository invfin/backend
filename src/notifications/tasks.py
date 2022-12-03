from typing import Dict

from celery import shared_task

from src.emailing.tasks import send_email_task
from src.notifications.outils.notifications import NotificationSystem


@shared_task()
def prepare_notification_task(object_related: Dict, notif_type: str):
    notification_info = NotificationSystem().notify(object_related, notif_type)
    for notif in notification_info:
        send_email_task.delay(**notif)
