from typing import List, Dict, Callable

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model
from django.utils.html import format_html, strip_tags
from django.template.loader import render_to_string
from django.template.defaultfilters import slugify

from apps.empresas.models import Company
from apps.escritos.models import Term
from apps.preguntas_respuestas.models import Question
from apps.public_blog.models import PublicBlog
from apps.seo.utils import generate_utm_url
from apps.socialmedias import constants
from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter

from .models import (
    BlogSharedHistorial,
    CompanySharedHistorial,
    NewsSharedHistorial,
    ProfileSharedHistorial,
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
    
    def news_content(self, content:Company=None):
        if not content:
            content = Company.objects.get_random_most_visited_clean_company()
        news = content.show_news[0]
        title = news['headline']
        description = news['summary']
        description = google_translator().translate(description, lang_src='en', lang_tgt='es')
        title = google_translator().translate(title, lang_src='en', lang_tgt='es')
        shared_model_historial = NewsSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "company_related": content,
            "shared_model_historial": shared_model_historial,
        }

    def company_content(self, content:Company=None):
        if not content:
            content = Company.objects.get_random_most_visited_clean_company()
        title = content.name
        description = f'{content.short_introduction} {content.description}'
        shared_model_historial = CompanySharedHistorial
        return {
            "title": title,
            "description": description,
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def question_content(self, content:Question=None):
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
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def term_content(self, content:Term=None):
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
            "link": FULL_DOMAIN + content.get_absolute_url(),
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }

    def publicblog_content(self, content:PublicBlog=None):
        if not content:
            content = PublicBlog.objects.get_random()
        title = content.title
        description = content.resume
        link = content.custom_url
        shared_model_historial = BlogSharedHistorial
        return {
            "title": title,
            "description": description,
            "link": link,
            "content_shared": content,
            "shared_model_historial": shared_model_historial,
        }
    
    def prepare_data_to_be_saved(self, social_media_fnct:Callable, content:Dict) -> Dict:
        social_media_post_response = social_media_fnct(**content)
        if type(social_media_post_response) == list:
            for post in social_media_post_response:
                post.update({"user": User.objects.get(username = 'Lucas')})
            return social_media_post_response
        else:
            social_media_post_response.update({"user": User.objects.get(username = 'Lucas')})
        return [social_media_post_response]

    def generate_content(self, social_medias:List, content:Dict) -> List:
        social_media_actions = {
            constants.FACEBOOK : self.facebook_poster.post_on_facebook,
            constants.TWITTER : self.twitter_poster.tweet,
            constants.INSTAGRAM : "",
            constants.YOUTUBE : "",
            constants.REDDIT : "",
            constants.WHATSAPP : "",
            constants.LINKEDIN : "",
            constants.PINTEREST : "",
            constants.TUMBLR : "",
        }
        social_media_content = []
        for social_media in social_medias:
            social_media_fnct = social_media_actions[social_media["platform"]]
            data_to_save = self.prepare_data_to_be_saved(social_media_fnct, content)
            social_media_content += data_to_save
            
        return social_media_content

    def save_post(self, data:List, shared_model_historial:Model):
        #Create a list inside the dict returned to generate multiples models and saved them in bulk
        default_manager = shared_model_historial._default_manager
        default_manager.bulk_create([shared_model_historial(**post) for post in data])
    
    @classmethod
    def share_content(cls, model_for_social_medias_content:int, social_medias:List, specific_model:Model = None):
        social_media_content = {
            constants.MODEL_QUESTION: cls.question_content,
            constants.MODEL_NEWS: cls.news_content,
            constants.MODEL_TERM: cls.term_content,
            constants.MODEL_BLOG: cls.publicblog_content,
            constants.MODEL_COMPANY: cls.company_content,
        }
        social_media_content_from_obj = social_media_content[model_for_social_medias_content]
        content_for_social_media = social_media_content_from_obj(specific_model)
        content_generated_and_posted = cls().generate_content(social_medias, content_for_social_media)
        shared_model_historial = content_for_social_media.pop("shared_model_historial")
        cls().save_post(content_generated_and_posted, shared_model_historial)
