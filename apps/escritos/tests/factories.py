from apps.escritos.models import Term, TermContent
from apps.escritos.tests.data import TERM, TERM_CONTENT, EMPTY_TERM


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
