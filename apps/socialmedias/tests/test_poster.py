import vcr

from django.conf import settings
from django.test import TestCase
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from apps.users.tests.factories import UserFactory
from apps.empresas.tests.factories import AppleExample
from apps.general.tests.factories import GenerateGeneralExample
from apps.escritos.tests.factories import GenerateEscritosExample
# from apps.public_blog.tests.factories

from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.poster import SocialPosting
from apps.socialmedias import constants

from .factories import GenerateSocialmediasExample


FULL_DOMAIN = settings.FULL_DOMAIN

poster_vcr = vcr.VCR(
    cassette_library_dir='cassettes/poster/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestPoster(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.question = Question.objects.create(**QUESTION)
        cls.user = UserFactory()
        GenerateGeneralExample.generate_all()
        GenerateSocialmediasExample.generate_all()
        GenerateEscritosExample.generate_all()
        cls.escritos_examples = GenerateEscritosExample
        # cls.public_blog = PublicBlog.objects.create(**PUBLICBLOG)
        cls.company = AppleExample.return_example()
    
    def test_company_content(self):
        with vcr.use_cassette('cassettes/company/retrieve/test_get_current_price.yaml'):
            company_poster = SocialPosting().company_content(self.company)
        self.assertEqual(
            company_poster, 
            {
                "title": self.company.name,
                "description": f'{self.company.short_introduction} {self.company.description}',
                "link": FULL_DOMAIN + self.company.get_absolute_url(),
                "content_shared": self.company,
                "shared_model_historial": CompanySharedHistorial,
            }
        )
    
    def test_term(self):
        term_poster = SocialPosting().term_content(self.escritos_examples.term)
        self.assertEqual(
            term_poster, 
            {
                "title": self.escritos_examples.term.title,
                "description": self.escritos_examples.term.resume,
                "link": FULL_DOMAIN + self.escritos_examples.term.get_absolute_url(),
                "content_shared": self.escritos_examples.term,
                "shared_model_historial": TermSharedHistorial,
            }
        )
    
    @poster_vcr.use_cassette(filter_post_data_parameters=['access_token'])
    def test_posting_specific_term_on_facebook(self):
        SocialPosting.share_content(
            constants.TERM,
            [
                {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            ],
            self.escritos_examples.term
        )
    
    # @poster_vcr.use_cassette(filter_post_data_parameters=['access_token'])
    def test_posting_specific_term_no_resume_on_facebook(self):
        SocialPosting.share_content(
            constants.TERM,
            [
                {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            ],
            self.escritos_examples.empty_term
        )
        
    # def test_blog(self):
    #     publicBlog = PublicBlog.objects.get_random()
    #     blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
    #     blog_response = publicBlog.title, 'https://inversionesyfinanzas.xyz' + publicBlog.get_absolute_url(), publicBlog.resume
    #     self.assertEqual(blog_poster, blog_response)

    # def test_question(self):
    #     question = Question.objects.get_random()
    #     question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()
    #     question_response= question.title, 'https://inversionesyfinanzas.xyz' + question.get_absolute_url(), question.content
    #     self.assertEqual(question_poster, question_response)

    

    # def test_clean_description(self):
    #     title, link, description = SocialPosting(QuestionSharedHistorial, self.question).generate_content()
    #     description = strip_tags(description)
    #     self.assertEqual(description, 'masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds sdfjhfb  fusd fvgsvd fsvd ')
