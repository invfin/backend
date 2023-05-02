from django.contrib.admin import site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.forms import (
    CharField,
    ChoiceField,
    DateTimeField,
    DateTimeInput,
    EmailField,
    Form,
    ModelForm,
    Textarea,
)

from src.content_creation import constants as content_creation_constants
from src.emailing.outils.emailing import EmailingSystem
from src.engagement_machine.outils.engagement import EngagementMachine
from src.web import constants
from src.web.models import WebsiteEmail


class AutomaticNewsletterForm(Form):
    web_email_type = ChoiceField(choices=constants.CONTENT_PURPOSES)
    content_object = ChoiceField(choices=content_creation_constants.MODELS_FOR_CONTENT)
    whom_to_send = ChoiceField(choices=constants.WHOM_TO_SEND_EMAIL)

    def create_newsletter(self):
        EngagementMachine().create_newsletter(**self.cleaned_data)


class ContactForm(Form):
    name = CharField(label="Nombre", required=True)
    email = EmailField(label="Email", required=True)
    message = CharField(widget=Textarea, label="Mensaje", required=True)

    def __init__(self, email_source: str = "soporte", *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.email_source = email_source

    def send_email(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        message = self.cleaned_data["message"]
        EmailingSystem.simple_email(
            f"Nuevo mensaje desde {self.email_source}",
            f"{name}<br>Con el email: {email}<br>{message}",
        )


class WebEmailForm(ModelForm):
    date_to_send = DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=DateTimeInput(attrs={"class": "form-control datetimepicker-input"}),
        required=False,
    )
    call_to_action = CharField(label="Call to action", required=False)
    call_to_action_url = CharField(label="Call to action url", required=False)

    class Meta:
        model = WebsiteEmail
        fields = [
            "title",
            "date_to_send",
            "content",
            "campaign",
            "whom_to_send",
            "users_selected",
            "call_to_action",
            "call_to_action_url",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["campaign"].widget = RelatedFieldWidgetWrapper(
            self.fields["campaign"].widget,
            self.instance._meta.get_field("campaign").remote_field,
            site,
        )
