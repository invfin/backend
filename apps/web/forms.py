from django.forms import (
    CharField,
    DateTimeField,
    DateTimeInput,
    EmailField,
    Form,
    ModelForm,
    Textarea,
    ChoiceField,
)
from django.contrib.admin import site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper

from apps.general.outils.emailing import EmailingSystem

from apps.web.models import WebsiteEmail
from apps.web.outils.engagement import EngagementMachine
from apps.web import constants
from apps.socialmedias import constants as socialmedias_constants


class AutomaticNewsletterForm(Form):
    web_email_type = ChoiceField(choices=constants.CONTENT_PURPOSES)
    content_object = ChoiceField(choices=socialmedias_constants.MODELS_FOR_CONTENT)
    whom_to_send = ChoiceField(choices=constants.WHOM_TO_SEND_EMAIL)

    def create_newsletter(self):
        EngagementMachine().create_newsletter(**self.cleaned_data)


class ContactForm(Form):
    name = CharField(label="Nombre", required=True)
    email = EmailField(label="Email", required=True)
    message = CharField(widget=Textarea, label="Mensaje", required=True)

    def send_email(self):
        name = self.cleaned_data["name"]
        email = self.cleaned_data["email"]
        message = self.cleaned_data["message"]
        EmailingSystem.simple_email(f"{name} con el email {email} ha enviado {message}", "Nuevo mensaje desde suport")


class WebEmailForm(ModelForm):
    date_to_send = DateTimeField(
        input_formats=["%d/%m/%Y %H:%M"],
        widget=DateTimeInput(attrs={"class": "form-control datetimepicker-input"}),
        required=False,
    )

    class Meta:
        model = WebsiteEmail
        fields = [
            "title",
            "date_to_send",
            "content",
            "campaign",
            "whom_to_send",
            "users_selected",
        ]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields["type_related"].widget = RelatedFieldWidgetWrapper(
            self.fields["type_related"].widget,
            self.instance._meta.get_field("type_related").remote_field,
            site,
        )
