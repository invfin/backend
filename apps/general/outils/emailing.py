from typing import Dict, Tuple, Type, Any

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from apps.general import constants

User = get_user_model()


class EmailingSystem:
    """
    Emailingsystem recieve information most of the times from celery, so all the data will be serialized.
    """

    # EMAIL_CONTACT = env("EMAIL_CONTACT", default=f"EMAIL_CONTACT@{CURRENT_DOMAIN}")
    # EMAIL_SUBJECT_PREFIX = env("EMAIL_SUBJECT_PREFIX",
    #                            default=f"EMAIL_SUBJECT_PREFIX@{CURRENT_DOMAIN}")
    # DEFAULT_EMAIL = env("DEFAULT_EMAIL", default=f"DEFAULT_EMAIL@{CURRENT_DOMAIN}")
    # EMAIL_NEWSLETTER = env("EMAIL_NEWSLETTER", default=f"EMAIL_NEWSLETTER@{CURRENT_DOMAIN}")
    # MAIN_EMAIL = env("MAIN_EMAIL", default=f"MAIN_EMAIL@{CURRENT_DOMAIN}")
    # EMAIL_ACCOUNTS = env("EMAIL_ACCOUNTS", default=f"EMAIL_ACCOUNTS@{CURRENT_DOMAIN}")
    # EMAIL_DEFAULT = env("EMAIL_DEFAULT", default=f"EMAIL_DEFAULT@{CURRENT_DOMAIN}")
    # EMAIL_SUGGESTIONS = env("EMAIL_SUGGESTIONS", default=f"EMAIL_SUGGESTIONS@{CURRENT_DOMAIN}")

    def __init__(self, is_for: str = None, web_objective: str = None) -> None:
        """
        is_for might be :
            -constants.EMAIL_FOR_PUBLIC_BLOG
            -constants.EMAIL_FOR_NOTIFICATION
            -constants.EMAIL_FOR_WEB
        """
        self.is_for = is_for
        self.web_objective = web_objective
        template = f"{is_for}/{web_objective}" if web_objective else is_for
        self.email_template = f"emailing/{template}.html"

    def _prepare_email_track(self, email_specifications: Dict[str, Any], receiver: Type) -> str:
        """
        email_specifications is a dict usually created from the model's property for_task
        receiver is an instance of User model queryed
        """
        email_model_instance = apps.get_model(
            email_specifications.pop("app_label"), email_specifications.pop("object_name"), require_ready=True
        )._default_manager.get(
            pk=email_specifications.pop("id")
        )  # email_model_instance is a Model inheritaded from BaseNewsletter
        email_track = email_model_instance.email_related.create(sent_to=receiver)
        # email_track is a Model inhertitaded from BaseEmail
        return email_track.encoded_url

    def _prepare_body(self, email: Dict[str, Any], receiver: Type) -> Dict:
        return {**email, "user": receiver, "image_tag": self._prepare_email_track(email, receiver)}

    def _prepare_sender(self, sender: str = None) -> str:
        if self.is_for == constants.EMAIL_FOR_PUBLIC_BLOG:
            email = settings.EMAIL_NEWSLETTER
        elif self.is_for == constants.EMAIL_FOR_NOTIFICATION:
            email = settings.EMAIL_DEFAULT
            sender = "InvFin"
        else:
            email = settings.MAIN_EMAIL
            sender = "Lucas - InvFin"

        return f"{sender} <{email}>"

    def _prepare_email(self, email: Dict[str, str], receiver: Type) -> Tuple[str, Dict]:
        sender = self._prepare_sender(email.pop("sender", None))
        base_body = self._prepare_body(email, receiver)
        return sender, base_body

    def enviar_email(self, email: Dict, receiver_id: int):
        # Needs to be defined what email expects
        receiver = User.objects.get(id=receiver_id)
        subject = email.pop("subject")
        sender, base_body = self._prepare_email(email, receiver)
        body = render_to_string(self.email_template, base_body)
        email_message = EmailMessage(subject, body, sender, [receiver.email])

        email_message.content_subtype = "html"
        email_message.send()

    @classmethod
    def simple_email(cls, subject: str, message: str, sent_by: str = "Web-automation"):
        return send_mail(subject, mark_safe(message), f"{sent_by} <{settings.EMAIL_DEFAULT}>", [settings.EMAIL_DEFAULT])

    @classmethod
    def html_link(cls, link: str, text: str, autocomplete_url: bool = False) -> str:
        if autocomplete_url:
            link = f"{settings.FULL_DOMAIN}{link}"
        return f'<a href="{link}" target="_blank">{text}</a>'
