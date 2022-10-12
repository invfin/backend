import vcr

from django.conf import settings
from django.test import TestCase

from apps.empresas.models import Company

from apps.escritos.models import Term, TermContent
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.constants import FACEBOOK
from apps.socialmedias.socialposter.facepy import Facebook

from apps.socialmedias.poster import SocialPosting


facebook_vcr = vcr.VCR(
    cassette_library_dir="cassettes/facebook/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
    filter_post_data_parameters=["access_token"],
)


class TestFacePoster(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.facebook_poster = Facebook(settings.NEW_FACEBOOK_ID, settings.NEW_FB_PAGE_ACCESS_TOKEN)
        # cls.company = AppleExample.return_example()
        GenerateSocialmediasExample.generate_all()
        cls.examples = GenerateSocialmediasExample

    @facebook_vcr.use_cassette
    def test_posting(self):
        with vcr.use_cassette("cassettes/company/retrieve/test_get_current_price.yaml"):
            content = SocialPosting().company_content(self.company)

        fb_response = self.facebook_poster.post_on_facebook(**content)
