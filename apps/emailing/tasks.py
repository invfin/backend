from typing import Dict

from config import celery_app

from apps.emailing.outils.emailing import EmailingSystem


@celery_app.task()
def send_email_task(email: Dict, receiver_id: int, is_for: str = "", web_objective: str = ""):
    return EmailingSystem(is_for, web_objective).enviar_email(email, receiver_id)
