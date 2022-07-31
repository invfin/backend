from django.forms import ModelForm

from .models import TermCorrection


class CreateCorrectionForm(ModelForm):
    class Meta:
        model = TermCorrection
        fields = [
            'title',
            'content',
            'term_content_related'
            ]

