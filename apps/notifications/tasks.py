from typing import Dict

from config import celery_app

from apps.emailing.tasks import send_email_task
from apps.notifications.outils.notifications import NotificationSystem


@celery_app.task()
def prepare_notification_task(object_related: Dict, notif_type: str):
    notification_info = NotificationSystem().notify(object_related, notif_type)
    for notif in notification_info:
        send_email_task.delay(**notif)
