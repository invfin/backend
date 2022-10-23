from celery import shared_task

from apps.general.outils.emailing import EmailingSystem
from apps.escritos.models import Term
from apps.socialmedias import constants as socialmedias_constants
from apps.web.outils.engagement import EngagementMachine
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail


@shared_task(autoretry_for=(Exception,), max_retries=3)
def notify_term_to_improve_task():
    """Filtering across all terms that doesn't already are completly clean it checks if it remains any.
    If one is found, it sends an email to remember that it must be cleaned.

    Returns
    -------
        None
            Send emails
    """
    terms_without_info = Term.objects.filter_checkings_not_seen("information_clean")
    if terms_without_info.exists():
        term = terms_without_info.first()
        term_link_html = EmailingSystem.html_link(term.admin_urls["change"], term.title)
        return EmailingSystem.simple_email(
            f"It's time to update {term}",
            f"You need to update {term_link_html} right now",
        )
    else:
        return EmailingSystem.simple_email(
            "No terms left to update",
            "All terms are correct",
        )


@shared_task(autoretry_for=(Exception,), max_retries=3)
def prepare_term_newsletter_task():
    """A task destinated to check across all the terms that are "clean"(the conent is correct and has a resume)
    and get one. From this term selected it creates a newsletter to be sent to all the users (maybe it would be needed
    to sent to just the users that are interested)

    Returns
    -------
        None
            It doesn't return anything. It will send an email to the admin notifying that a new newsletter is ready or
            that there isn't any term ready
    """
    term_for_newsletter = Term.objects.term_ready_newsletter()
    if term_for_newsletter:
        if WebsiteEmail.objects.filter(
            content_type=term_for_newsletter.content_type.id, object_id=term_for_newsletter.id
        ).exists():
            subject = f"You need to clean a new term before creating a new newsletter"
            message = f"There aren terms ready to be sent, you must update one"
            notify_term_to_improve_task.delay()
        else:
            web_email = EngagementMachine().create_newsletter(
                web_email_type=web_constants.CONTENT_FOR_NEWSLETTER_TERM,
                content_object=socialmedias_constants.TERM_FOR_CONTENT,
                whom_to_send=web_constants.WHOM_TO_SEND_EMAIL_TYPE_RELATED,
            )
            term_link_html = EmailingSystem.html_link(web_email.edit_url, term_for_newsletter.title)
            subject = f"{term_for_newsletter} is ready to be sent as a newsletter"
            message = f"You need to update {term_link_html} to be ready to be sent as a newsletter"

    else:
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"

    return EmailingSystem.simple_email(subject, message)
