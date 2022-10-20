from celery import shared_task

from django.conf import settings
from django.core.mail import send_mail

from apps.escritos.models import Term


@shared_task(autoretry_for=(Exception,), max_retries=3)
def notify_term_to_improve():
    terms_without_info = Term.objects.filter_checkings_not_seen("information_clean")
    if terms_without_info.exists():
        term = terms_without_info.first()
        return send_mail(
            f"It's time to update {term}",
            f"You need to update {term} right now {term.shareable_link}",
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT],
        )
    else:
        return send_mail(
            "No terms left to update",
            "All terms are correct",
            settings.EMAIL_DEFAULT,
            [settings.EMAIL_DEFAULT],
        )
