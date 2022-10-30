from django.forms import ModelForm, models

from apps.general.forms import BaseEscritoForm
from .models import TermCorrection, Term, TermContent


class CreateCorrectionForm(ModelForm):
    class Meta:
        model = TermCorrection
        fields = ["title", "content", "term_content_related"]


class TermAndTermContentForm(BaseEscritoForm):
    class Meta(BaseEscritoForm.Meta):
        model = Term

    def save(self, *args, **krags):
        self.instance.modify_checking("information_clean", True)
        return super().save(*args, **krags)


term_content_formset = models.inlineformset_factory(
    Term,
    TermContent,
    fields=["title", "order", "content"],
    extra=0,
    can_delete=False,
)
