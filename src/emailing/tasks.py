from typing import Dict

from celery import shared_task

from src.emailing.outils.emailing import EmailingSystem


@shared_task()
def send_email_task(email: Dict, receiver_id: int, is_for: str = "", web_objective: str = ""):
    return EmailingSystem(is_for, web_objective).rich_email(email, receiver_id)
