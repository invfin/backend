from typing import Any, Dict, List, Optional, Tuple, Type, Union

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from src.emailing import constants
from src.web import constants as web_constants

User = get_user_model()


class EmailSender:
    is_for: str
    web_objective: str

    def __init__(self, is_for: str, web_objective: str) -> None:
        self.is_for = is_for
        self.web_objective = web_objective

    def __call__(self, sender: str = "") -> str:
        if self._is_for_public_blog():
            return self._return_public_blog_author_as_sender(sender)
        elif self._is_for_notifications():
            return self._return_default_sender()
        else:
            return self._return_lucas_as_sender()

    def _is_for_public_blog(self) -> bool:
        return self.is_for == constants.EMAIL_FOR_PUBLIC_BLOG

    def _is_for_notifications(self) -> bool:
        return self.is_for == constants.EMAIL_FOR_NOTIFICATION

    def _return_public_blog_author_as_sender(self, sender: str) -> str:
        return self._return_email_and_sender_name(settings.EMAIL_NEWSLETTER, sender)

    def _return_default_sender(self) -> str:
        return self._return_email_and_sender_name(settings.EMAIL_DEFAULT, "InvFin")

    def _return_lucas_as_sender(self) -> str:
        if self.web_objective in web_constants.WEB_OBJECTIVES:
            email = settings.EMAIL_SUGGESTIONS
        else:
            email = settings.MAIN_EMAIL
        return self._return_email_and_sender_name(email, "Lucas - InvFin")

    @staticmethod
    def _return_email_and_sender_name(email: str, sender: str) -> str:
        return f"{sender} <{email}>"


class EmailingSystem:
    """
    Emailingsystem recieve information most of the times from celery, so all the data will be serialized.
    """

    is_for: str
    web_objective: str
    email_template: str

    def __init__(self, is_for: str = "", web_objective: str = "") -> None:
        """
        is_for might be :
            -constants.EMAIL_FOR_PUBLIC_BLOG
            -constants.EMAIL_FOR_NOTIFICATION
            -constants.EMAIL_FOR_WEB
        """
        self.is_for = is_for
        self.verify_there_is_web_objective(web_objective)
        self.web_objective = web_objective.split("-")[0]
        self.email_template = self.get_email_template()

    def verify_there_is_web_objective(self, web_objective) -> None:
        if self.is_for_the_website() and not web_objective:
            raise NotImplementedError("You must set a web_objective")

    def is_for_the_website(self) -> bool:
        return self.is_for == constants.EMAIL_FOR_WEB

    def get_email_template(self) -> str:
        template = f"{self.is_for}/{self.web_objective}" if self.web_objective else self.is_for
        return f"{template}.html"

    def _prepare_email_track(self, app_label: str, object_name: str, object_id: int, receiver: Type) -> str:
        """
        email_specifications is a dict usually created from the model's property for_task
        receiver is an instance of User model queryed
        """
        email_model = apps.get_model(app_label, object_name, require_ready=True)
        # email_model_instance is a Model inheritaded from BaseEmail
        email_model_instance = email_model._default_manager.get(pk=object_id)
        email_track = email_model_instance.email_related.create(sent_to=receiver)
        # email_track is a Model inhertitaded from BaseTrackEmail
        return email_track.encoded_url

    @staticmethod
    def append_slash_to_call_to_action_url(call_to_action_url: str) -> str:
        # if not call_to_action_url.startswith("/"):
        #     call_to_action_url = f"/{call_to_action_url}"
        return call_to_action_url

    @classmethod
    def build_call_to_action_url(cls, base_call_to_action_url: str) -> str:
        if base_call_to_action_url:
            call_to_action_url = cls.append_slash_to_call_to_action_url(base_call_to_action_url)
            # TODO Add utm
            return call_to_action_url
        return ""

    @classmethod
    def get_call_to_action_parameters(cls, email: Dict[str, Any]) -> Tuple[str, str]:
        call_to_action = email.pop("call_to_action", "")
        base_call_to_action_url = email.pop("call_to_action_url", "")
        return call_to_action, base_call_to_action_url

    def _prepare_call_to_action(self, email: Dict[str, Any]) -> Dict[str, Optional[str]]:
        call_to_action, base_call_to_action_url = self.get_call_to_action_parameters(email)
        call_to_action_url = self.build_call_to_action_url(base_call_to_action_url)
        return {"call_to_action": call_to_action, "call_to_action_url": call_to_action_url}

    @classmethod
    def get_email_track_parameters(cls, email: Dict[str, Any]) -> Tuple[str, str, int]:
        return email.pop("app_label"), email.pop("object_name"), email.pop("id")

    def _prepare_content(self, email: Dict[str, Any], receiver: Type) -> Dict:
        app_label, object_name, object_id = self.get_email_track_parameters(email)
        image_tag = self._prepare_email_track(app_label, object_name, object_id, receiver)
        cta = self._prepare_call_to_action(email)
        return {
            **email,
            "user": receiver,
            "image_tag": image_tag,
            **cta,
        }

    def _prepare_email(self, email: Dict[str, str], receiver: Type) -> Tuple[str, Dict]:
        sender = EmailSender(self.is_for, self.web_objective)(email.pop("sender", ""))
        content = self._prepare_content(email, receiver)
        return sender, content

    def rich_email(self, email: Dict[str, Union[str, int]], receiver_id: int):
        """
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
