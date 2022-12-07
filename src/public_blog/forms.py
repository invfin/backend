from django.forms import ChoiceField, ModelForm

from .models import PublicBlog, WritterProfile


class WritterProfileForm(ModelForm):
    class Meta:
        model = WritterProfile
        fields = [
            "long_description",
            "facebook",
            "twitter",
            "insta",
            "youtube",
            "linkedin",
            "tiktok",
        ]
        labels = {
            "insta": "Instagram",
        }


class PublicBlogForm(ModelForm):
    status = ChoiceField(choices=((1, "Publicar"), (2, "Guardar como borrador"), (3, "Programar")))

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
