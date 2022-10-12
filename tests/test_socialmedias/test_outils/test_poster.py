import vcr
import pytest

from django.conf import settings

from apps.socialmedias.models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)
from apps.socialmedias.outils.poster import SocialPosting
from apps.socialmedias import constants


FULL_DOMAIN = settings.FULL_DOMAIN

poster_vcr = vcr.VCR(
    cassette_library_dir="cassettes/poster/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@pytest.mark.django_db
@pytest.mark.usefixtures("clean_company")
class TestSocialPosting:

    def test_create_link(self):
        company_created_link = SocialPosting().create_link(self.clean_company)
        print(company_created_link)

    @poster_vcr.use_cassette
    def test_news_content(self):
        news_content = SocialPosting().news_content(self.clean_company)
        print(news_content)

    def test_company_content(self):
        with vcr.use_cassette("cassettes/company/retrieve/test_get_current_price.yaml"):
            company_poster = SocialPosting().company_content(self.clean_company)
        assert company_poster == {
            "title": self.clean_company.name,
            "description": f"{self.clean_company.short_introduction} {self.clean_company.description}",
            "link": FULL_DOMAIN + self.clean_company.get_absolute_url(),
            "content_shared": self.clean_company,
            "shared_model_historial": CompanySharedHistorial,
        }

    def test_term(self):
        term_poster = SocialPosting().term_content(self.escritos_examples.term)
        assert term_poster == {
            "title": self.escritos_examples.term.title,
            "description": self.escritos_examples.term.resume,
            "link": FULL_DOMAIN + self.escritos_examples.term.get_absolute_url(),
            "content_shared": self.escritos_examples.term,
            "shared_model_historial": TermSharedHistorial,
        }

    @poster_vcr.use_cassette(filter_post_data_parameters=["access_token"])
    def test_posting_specific_term_on_facebook(self):
        SocialPosting().share_content(
            constants.TERM,
            [
                {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            ],
            self.escritos_examples.term,
        )

    @poster_vcr.use_cassette(filter_post_data_parameters=["access_token"])
    def test_posting_specific_term_no_resume_on_facebook(self):
        SocialPosting().share_content(
            constants.TERM,
            [
                {"platform": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT},
            ],
            self.escritos_examples.empty_term,
        )

    # def test_blog(self):
    #     publicBlog = PublicBlog.objects.get_random()
    #     blog_poster = SocialPosting(BlogSharedHistorial, publicBlog).generate_content()
    #     blog_response = publicBlog.title, 'https://inversionesyfinanzas.xyz' + publicBlog.get_absolute_url(), publicBlog.resume
    #     assert blog_poster == blog_response

    # def test_question(self):
    #     question = Question.objects.get_random()
    #     question_poster = SocialPosting(QuestionSharedHistorial, question).generate_content()
    #     question_response= question.title, 'https://inversionesyfinanzas.xyz' + question.get_absolute_url(), question.content
    #     assert question_poster == question_response

    # def test_clean_description(self):
    #     title, link, description = SocialPosting(QuestionSharedHistorial, self.question).generate_content()
    #     description = strip_tags(description)
    #     assert description == 'masidf sdbf sdf sfg fdïfdsf  hbsdf ónjbfds ds ds sdfjhfb  fusd fvgsvd fsvd '
