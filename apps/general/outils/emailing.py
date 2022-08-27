from typing import Dict, Tuple

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

User = get_user_model()

from apps.general import constants


class EmailingSystem():
    """
    Emailingsystem recieve information most of the times from celery, so all the data will be serialized.
    """
    email_contacto = settings.EMAIL_CONTACT
    email_lucas = settings.MAIN_EMAIL
    email_cuentas = settings.EMAIL_ACCOUNTS
    email_sugerencias = settings.EMAIL_SUGGESTIONS
    email_no_responder = settings.EMAIL_DEFAULT

    def __init__(self, is_for:str=None, web_objective:str=None) -> None:
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

    def _prepare_email_track(self, email_specifications:Dict[str, str], receiver:User) -> str:
        """
        email_specifications is a dict usually created from the model's property for_task
        receiver is an instance of User model queryed
        """
        email_model_instance = apps.get_model(
            email_specifications.pop("app_label"),
            email_specifications.pop("object_name"),
            require_ready=True
        )._default_manager.get(
            pk = email_specifications.pop("id")
        ) # email_model_instance is a Model inheritaded from BaseNewsletter
        email_track = email_model_instance.email_related.create(sent_to=receiver)
        # email_track is a Model inhertitaded from BaseEmail
        return email_track.encoded_url

    def _prepare_email(self, email:Dict[str, str], receiver:User) -> Tuple[str, str]:
        sender = self.prepare_sender(email.pop("sender", None))
        message = self.prepare_message(email, receiver)
        return message, sender

    def prepare_sender(self, sender:str=None) -> str:
        if self.is_for == constants.EMAIL_FOR_PUBLIC_BLOG:
            email = settings.EMAIL_NEWSLETTER
        elif self.is_for == constants.EMAIL_FOR_NOTIFICATION:
            email = settings.EMAIL_DEFAULT
            sender = "InvFin"
        else:
            email = "Lucas - InvFin"

        return f"{sender} <{email}>"

    def prepare_message(self, email:Dict[str, str], receiver:User) -> str:
        base_message = {
            **email,
            "user": receiver,
            'image_tag': self._prepare_email_track(email, receiver)
        }
        return render_to_string(self.email_template, base_message)

    def enviar_email(self, email:Dict, receiver_id:int):
        receiver = User.objects.get(id = receiver_id)
        subject = email.pop('title')
        message, sender = self._prepare_email(email, receiver)

        email_message = EmailMessage(
            subject,
            message,
            sender,
            [receiver.email]
        )

        email_message.content_subtype = "html"
        email_message.send()

    def simple_email(self, subject:str, message:str):
        return send_mail(subject, message, self.email_no_responder, [self.email_no_responder])
