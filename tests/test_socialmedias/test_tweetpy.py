from django.test import TestCase

import vcr

from src.empresas.models import Company
from src.escritos.models import Term
from src.preguntas_respuestas.models import Question
from src.public_blog.models import PublicBlog

twitter_vcr = vcr.VCR(
    cassette_library_dir="cassettes/twitter/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


class TestPoster(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.term = Term.objects.create(
            title="term",
            resume="resumen",
        )
        cls.question = Question.objects.create(
            title="question",
            content="pregutna larga",
        )
        cls.publicBlog = PublicBlog.objects.create(
            title="public blog",
            resume="blog resumido",
            content="contenido largo del blog",
        )
        cls.company = Company.objects.create(name="Apple", ticker="AAPL")
        cls.term2 = Term.objects.create(
            title="term 2",
            resume="resumen 2",
        )
        cls.question2 = Question.objects.create(
            title="question 2",
            content="pregutna larga 2",
        )
        cls.publicBlog2 = PublicBlog.objects.create(
            title="public blog 2",
            resume="blog resumido 2",
            content="contenido largo del blog 2",
        )
        cls.company2 = Company.objects.create(name="Intel", ticker="INTC")
