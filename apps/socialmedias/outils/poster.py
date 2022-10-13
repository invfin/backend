from typing import List, Dict, Callable, Type, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.utils.html import format_html, strip_tags

from apps.empresas.models import Company
from apps.empresas.outils.retrieve_data import RetrieveCompanyData
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.socialmedias import constants
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter
from apps.socialmedias.outils.content_creation import ContentCreation
from ..models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    QuestionSharedHistorial,
    TermSharedHistorial,
)

from apps.translate.google_trans_new import google_translator

User = get_user_model()
DOMAIN = settings.CURRENT_DOMAIN
FULL_DOMAIN = settings.FULL_DOMAIN

# render_to_string(self.newsletter_template, {
#             'usuario': receiver,
#             'introduction':introduction,
#             'content':content,
#             'despedida':despedida,
#             'image_tag':image_tag
#         })


class SocialPosting:
    facebook_poster = Facebook(settings.NEW_FACEBOOK_ID, settings.NEW_FB_PAGE_ACCESS_TOKEN)
    # instagram_poster
    twitter_poster = Twitter()
    # youtube_poster

    def create_link(self, content: Type, use_default: bool = True) -> str:
        if use_default:
            return FULL_DOMAIN + content.get_absolute_url()
        return content.custom_url

    def create_title(self, title):
        pass

    def news_content(self, content: Company = None, **kwargs):
        if not content:
            content = Company.objects.get_random_most_visited_clean_company(kwargs)

        news = RetrieveCompanyData(content).get_company_news()
        if not news:
            return self.news_content(kwargs={"exclude": {"id": content.id}})
        news = news[0]
        title = news["headline"]
        description = news["summary"]
        description = google_translator().translate(description, lang_src="en", lang_tgt="es")
        title = google_translator().translate(title, lang_src="en", lang_tgt="es")
        shared_model_historial = NewsSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": self.create_link(content),
            "company_related": content,
            "shared_model_historial": shared_model_historial,
        }

    def company_content(self, content: Company = None) -> Dict[str, Union[str, Type]]:
        if not content:
            content = Company.objects.get_random_most_visited_clean_company()
        title = content.name
        description = f"{content.short_introduction} {content.description}"
        shared_model_historial = CompanySharedHistorial
        return {
            "title": title,
            "description": description,
            "link": self.create_link(content),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def question_content(self, content: Question = None) -> Dict[str, Union[str, Type]]:
        if not content:
            content = Question.objects.get_random()
        description = content.content
        title = content.title
        description = strip_tags(format_html(description))
        title = strip_tags(format_html(title))
        shared_model_historial = QuestionSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": self.create_link(content),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def term_content(self, content: Term = None) -> Dict[str, Union[str, Type]]:
        if not content:
            content = Term.objects.random_clean()
        title = content.title
        resume = content.resume
        description = resume if resume else f"{title} "
        for index, term_content in enumerate(content.term_content_parts.all()):
            description = f"""{description}
            {index}.-{term_content.title}
            """
        shared_model_historial = TermSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": self.create_link(content),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def publicblog_content(self, content: PublicBlog = None) -> Dict[str, Union[str, Type]]:
        if not content:
            content = PublicBlog.objects.get_random()
        title = content.title
        description = content.resume
        shared_model_historial = BlogSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": self.create_link(content, False),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def prepare_data_to_be_saved(self, social_media_fnct: Callable, content: Dict) -> Dict:
        social_media_post_response = social_media_fnct(**content)
        if "multiple_posts" in social_media_post_response:
            social_media_post_response = social_media_post_response["posts"]
            for post in social_media_post_response:
                post.update({"user": User.objects.get(username="Lucas")})
            return social_media_post_response

        else:
            social_media_post_response.update({"user": User.objects.get(username="Lucas")})
        return [social_media_post_response]

    def generate_content(self, social_medias: List, content: Dict) -> List:
        social_media_actions = {
            constants.FACEBOOK: self.facebook_poster.post_on_facebook,
            constants.TWITTER: self.twitter_poster.tweet,
            constants.INSTAGRAM: "",
            constants.YOUTUBE: "",
            constants.REDDIT: "",
            constants.WHATSAPP: "",
            constants.LINKEDIN: "",
            constants.PINTEREST: "",
            constants.TUMBLR: "",
        }
        social_media_content = []
        for social_media in social_medias:
            social_media_fnct = social_media_actions[social_media["platform"]]
            data_to_save = self.prepare_data_to_be_saved(social_media_fnct, content)
            social_media_content += data_to_save

        return social_media_content

    def save_post(self, data, shared_model_historial: Model):
        # Create a list inside the dict returned to generate multiples models and saved them in bulk
        default_manager = shared_model_historial._default_manager
        default_manager.bulk_create([shared_model_historial(**post) for post in data])

    def share_content(
        self, model_for_social_medias_content: int, social_medias: List, specific_model: Model = None
    ) -> Dict[str, Union[str, Type]]:
        social_media_content = {
            constants.QUESTION: self.question_content,
            constants.NEWS: self.news_content,
            constants.TERM: self.term_content,
            constants.BLOG: self.publicblog_content,
            constants.COMPANY: self.company_content,
        }
        social_media_content_from_obj = social_media_content[model_for_social_medias_content]
        content_for_social_media = social_media_content_from_obj(specific_model)
        content_generated_and_posted = self.generate_content(social_medias, content_for_social_media)
        shared_model_historial = content_for_social_media.pop("shared_model_historial")
        self.save_post(content_generated_and_posted, shared_model_historial)
