from celery import shared_task

from apps.escritos.models import Term
from apps.general.outils.emailing import EmailingSystem
from apps.socialmedias import constants as socialmedias_constants
from apps.web import constants as web_constants
from apps.web.models import WebsiteEmail
from apps.web.outils.engagement import EngagementMachine


@shared_task(autoretry_for=(Exception,), max_retries=3)
def notify_term_to_improve_task():
    """Filtering across all terms that doesn't already are completly clean it checks if it remains any.
    If one is found, it sends an email to remember that it must be cleaned.

    Returns
    -------
        None
            Send emails
    """
    terms_without_info = Term.objects.to_be_cleaned()
    if terms_without_info.exists():
        term = terms_without_info.first()
        terms_without_info_but_already_requested = Term.objects.filter_checkings(
            [
                {"request_improvement": True},
                {"information_clean": False},
            ]
        ).exclude(pk=term.pk)
        term.modify_checking("request_improvement", True)
        term_link_html = EmailingSystem.html_link(term.admin_urls["change"], term.title)
        content = f"You need to update {term_link_html} right now."
        subject = f"It's time to update {term}"
        if terms_without_info_but_already_requested:
            subject = f"{subject} and also {terms_without_info_but_already_requested.count()} more"
            content = f"{content} Furtheremore you have to improve:"
            for term_left in terms_without_info_but_already_requested:
                term_left_link_html = EmailingSystem.html_link(term_left.admin_urls["change"], term_left.title)
                content = f"{content}\n {term_left_link_html}"
    else:
        content = "No terms left to update"
        subject = "All terms are correct"
    return EmailingSystem.simple_email(subject, content)


@shared_task(autoretry_for=(Exception,), max_retries=3)
def prepare_term_newsletter_task():
    """A task destinated to check across all the terms that are "clean"(the content is correct and has a resume)
    and get one. From this term selected it creates a newsletter to be sent to all the users (maybe it would be needed
    to sent to just the users that are interested)

    Returns
    -------
        None
            It doesn't return anything. It will send an email to the admin notifying that a new newsletter is ready or
            that there isn't any term ready
    """
    term_for_newsletter = Term.objects.term_ready_newsletter()
    notify = True
    if term_for_newsletter:
        if WebsiteEmail.objects.filter(
            content_type=term_for_newsletter.content_type.id, object_id=term_for_newsletter.id
        ).exists():
            subject = "You need to clean a new term before creating a new newsletter"
            message = "There aren terms ready to be sent, you must update one"
        else:
            web_email = EngagementMachine().create_newsletter(
                web_email_type=web_constants.CONTENT_FOR_NEWSLETTER_TERM,
                content_object=socialmedias_constants.TERM_FOR_CONTENT,
                whom_to_send=web_constants.WHOM_TO_SEND_EMAIL_CAMPAIGN_RELATED,
            )
            term_link_html = EmailingSystem.html_link(web_email.edit_url, term_for_newsletter.title)
            subject = f"{term_for_newsletter} is ready to be sent as a newsletter"
            message = f"You need to update {term_link_html} to be ready to be sent as a newsletter"
            notify = False
    else:
        subject = "There are no terms ready for newsletters"
        message = "Create newsletters"

    if notify:
        notify_term_to_improve_task.delay()
    return EmailingSystem.simple_email(subject, message)
