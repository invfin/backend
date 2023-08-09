from django.forms import ChoiceField, ModelForm

from .models import PublicBlog, WriterProfile


class WriterProfileForm(ModelForm):
    class Meta:
        model = WriterProfile
        fields = [
            "long_description",
            "facebook",
            "twitter",
            "instagram",
            "youtube",
            "linkedin",
            "tiktok",
        ]


class PublicBlogForm(ModelForm):
    status = ChoiceField(
        choices=((1, "Publicar"), (2, "Guardar como borrador"), (3, "Programar"))
    )

    class Meta:
        model = PublicBlog
        fields = ["title", "resume", "status", "send_as_newsletter", "content"]
        labels = {
            "title": "Título",
            "resume": "Resumen",
            "status": "Estatus",
            "send_as_newsletter": "¿Quieres enviar este blog a tus lectores por email?",
            "content": "Cuerpo",
        }
