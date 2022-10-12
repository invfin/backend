import vcr

from django.test import TestCase

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.socialposter.tweetpy import Twitter

from apps.socialmedias.poster import SocialPosting


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
