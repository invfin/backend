from model_bakery import baker

from apps.escritos.tests.data import TERM, TERM_CONTENT, EMPTY_TERM
from apps.escritos.models import (
FavoritesTermsHistorial,
FavoritesTermsList,
Term,
TermContent,
TermCorrection,
TermsComment,
TermsRelatedToResume,
)


favs_terms_historial = baker.make(FavoritesTermsHistorial)
favs_terms_list = baker.make(FavoritesTermsList)


term_correction = baker.make(TermCorrection)
term_comment = baker.make(TermsComment)
term_to_resume = baker.make(TermsRelatedToResume)


class GenerateEscritosExample:
    term = Term.objects.get(id=TERM['id'])
    term_content = TermContent.objects.all()
    empty_term = Term.objects.get(id=EMPTY_TERM['id'])

    @classmethod
    def generate_term(cls):
        Term.objects.get_or_create(**EMPTY_TERM)
        Term.objects.get_or_create(**TERM)

    @classmethod
    def generate_term_content(cls):
        for info in TERM_CONTENT:
            TermContent.objects.get_or_create(**info)

    @classmethod
    def generate_all(cls):
        cls.generate_term()
        cls.generate_term_content()
