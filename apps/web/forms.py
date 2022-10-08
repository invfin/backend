from django.forms import (
    CharField,
    DateTimeField,
    DateTimeInput,
    EmailField,
    Form,
    ModelForm,
    Textarea,
)

from apps.general.outils.emailing import EmailingSystem

from apps.web.models import WebsiteEmail


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
        widget=DateTimeInput(attrs={"class": "form-control datetimepicker-input", "id": "datetimepicker1"}),
    )

    class Meta:
        model = WebsiteEmail
        fields = "__all__"
