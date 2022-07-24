from apps.escritos.models import Term, TermContent
from apps.escritos.tests.data import TERM, TERM_CONTENT


class GenerateEscritosExample:
    term = Term.objects.all()
    term_content = TermContent.objects.all()
    
    @classmethod
    def generate_term(cls):
        Term.objects.create(**TERM)

    @classmethod
    def generate_term_content(cls):
        for info in TERM_CONTENT:
            TermContent.objects.create(**info)
    
    @classmethod
    def generate_all(cls):
        cls.generate_term()
        cls.generate_term_content()