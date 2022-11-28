from typing import Any, Dict, List, Tuple, Type, Union

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from apps.emailing import constants
from apps.web import constants as web_constants

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

    def __init__(self, is_for: str = "", web_objective: str = "") -> None:
        """
        is_for might be :
            -constants.EMAIL_FOR_PUBLIC_BLOG
            -constants.EMAIL_FOR_NOTIFICATION
            -constants.EMAIL_FOR_WEB
        """
        self.is_for = is_for
        if is_for == constants.EMAIL_FOR_WEB and not web_objective:
            raise NotImplementedError("You must set a web_objective")
        self.web_objective = web_objective.split("-")[0]
        template = f"{is_for}/{web_objective}" if web_objective else is_for
        self.email_template = f"{template}.html"

    def _prepare_email_track(self, email_specifications: Dict[str, Any], receiver: Type) -> str:
        """
        email_specifications is a dict usually created from the model's property for_task
        receiver is an instance of User model queryed
        """
        email_model_instance = apps.get_model(
            email_specifications.pop("app_label"), email_specifications.pop("object_name"), require_ready=True
        )._default_manager.get(
            pk=email_specifications.pop("id")
        )  # email_model_instance is a Model inheritaded from BaseEmail
        email_track = email_model_instance.email_related.create(sent_to=receiver)
        # email_track is a Model inhertitaded from BaseTrackEmail
        return email_track.encoded_url

    def _prepare_content(self, email: Dict[str, Any], receiver: Type) -> Dict:
        return {**email, "user": receiver, "image_tag": self._prepare_email_track(email, receiver)}

    def _prepare_sender(self, sender: str = "") -> str:
        if self.is_for == constants.EMAIL_FOR_PUBLIC_BLOG:
            email = settings.EMAIL_NEWSLETTER
        elif self.is_for == constants.EMAIL_FOR_NOTIFICATION:
            email = settings.EMAIL_DEFAULT
            sender = "InvFin"
        else:
            sender = "Lucas - InvFin"
            if self.web_objective in web_constants.WEB_OBJECTIVES:
                email = settings.EMAIL_SUGGESTIONS
            else:
                email = settings.MAIN_EMAIL

        return f"{sender} <{email}>"

    def _prepare_email(self, email: Dict[str, str], receiver: Type) -> Tuple[str, Dict]:
        sender = self._prepare_sender(email.pop("sender", ""))
        content = self._prepare_content(email, receiver)
        return sender, content

    def enviar_email(self, email: Dict[str, Union[str, int]], receiver_id: int):
        """Recieves the email that has to be sent and the id of the user to sent the email to.

        Parameters
        ----------
            email : Dict[str, Union[str, int]]
                The email's data to be sent
                Example: {
                    "subject": str
                        The subject of the email
                    "content": str
                        The content of the email
                    "sender":
                        The one who send the email
                    "app_label": str
                        The app where the model lives
                    "object_name": str
                        The model to retrieve
                    "id": int
                        The id of the obj from the model to create the tracker tag
                }

            receiver_id : int
                The id of the user to recieve the email
        """
        receiver = User.objects.get(id=receiver_id)
        subject = email.pop("subject")
        sender, content = self._prepare_email(email, receiver)
        content.update({"full_domain": settings.FULL_DOMAIN})
        final_content = render_to_string(self.email_template, content)
        self.send_email(subject, final_content, sender, [receiver.email])

    @classmethod
    def send_email(
        cls,
        subject: str,
        body: str,
        from_email: str,
        to: Union[List, Tuple],
        bcc: Union[List, Tuple] = [],
        connection=None,
        attachments: List = [],
        headers: Dict = {},
        cc: Union[List, Tuple] = [],
        reply_to: Union[List, Tuple] = [],
    ):
        email_message = EmailMessage(subject, body, from_email, to, bcc, connection, attachments, headers, cc, reply_to)
        email_message.content_subtype = "html"
        email_message.send()

    @classmethod
    def simple_email(cls, subject: str, message: str, sent_by: str = "Web-automation"):
        body = render_to_string("web/internal.html", {"content": message})
        return cls.send_email(subject, body, f"{sent_by} <{settings.EMAIL_DEFAULT}>", [settings.EMAIL_DEFAULT])

    @classmethod
    def html_link(cls, link: str, text: str, autocomplete_url: bool = False) -> str:
        if autocomplete_url:
            link = f"{settings.FULL_DOMAIN}{link}"
        return f'<a href="{link}" target="_blank">{text}</a>'
