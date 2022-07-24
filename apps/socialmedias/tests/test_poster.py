import vcr

from django.conf import settings
from django.test import TestCase
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe

from apps.users.tests.factories import UserFactory
from apps.empresas.tests.factories import AppleExample
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


FULL_DOMAIN = settings.FULL_DOMAIN

poster_vcr = vcr.VCR(
    cassette_library_dir='cassettes/poster/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class PosterTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # cls.question = Question.objects.create(**QUESTION)
        cls.user = UserFactory()
        GenerateEscritosExample.generate_all()
        cls.term = GenerateEscritosExample
        # cls.public_blog = PublicBlog.objects.create(**PUBLICBLOG)
        cls.company = AppleExample.return_example()
    
    def test_company(self):
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
    
    @poster_vcr.use_cassette
    def test_posting_question(self):
        SocialPosting.share_content(
            constants.MODEL_TERM,
            [
                {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
                {"platform": constants.TWITTER, "post_type": constants.POST_TYPE_TEXT}
            ]
        )
        content = SocialPosting().company_content(self.term)
        fb_response = self.facebook_poster.post_on_facebook(**content)
        print(fb_response)
        
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

    # def test_term(self):
    #     term = Term.objects.get_random()
    #     term_poster = SocialPosting(TermSharedHistorial, term).generate_content()
    #     term_response = term.title, 'https://inversionesyfinanzas.xyz' + term.get_absolute_url(), term.resume
    #     self.assertEqual(term_poster, term_response)

    # def test_clean_description(self):
    #     title, link, description = SocialPosting(QuestionSharedHistorial, self.question).generate_content()
    #     description = strip_tags(description)
    #     self.assertEqual(description, 'masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds sdfjhfb  fusd fvgsvd fsvd ')
