import random
from typing import List, Dict, Callable, Type, Union

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Model


from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter
from apps.socialmedias.outils.content_creation import (
    ContentCreation,
    TermContentCreation,
    QuestionContentCreation,
    PublicBlogContentCreation,
)
from apps.socialmedias.outils.company_content_creation import (
    CompanyContentCreation,
    CompanyNewsContentCreation,
)
from apps.socialmedias import constants


User = get_user_model()


class SocialPosting:
    facebook: Facebook = Facebook(
        settings.NEW_FACEBOOK_ID,
        settings.NEW_FB_PAGE_ACCESS_TOKEN,
        "InversionesyFinanzas",
    )
    twitter: Twitter = Twitter(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    instagram: Type = None
    youtube: Type = None
    socialmedias_map: Dict = {
        constants.FACEBOOK: facebook,
        constants.TWITTER: twitter,
        constants.INSTAGRAM: "",
        constants.YOUTUBE: "",
        constants.REDDIT: "",
        constants.WHATSAPP: "",
        constants.LINKEDIN: "",
        constants.PINTEREST: "",
        constants.TUMBLR: "",
    }
    socialmedia_creators_map: Dict = {
        constants.QUESTION: QuestionContentCreation,
        constants.NEWS: CompanyNewsContentCreation,
        constants.TERM: TermContentCreation,
        constants.PUBLIC_BLOG: PublicBlogContentCreation,
        constants.COMPANY: CompanyContentCreation,
    }

    def get_creator(self, content_object: int) -> Type:
        return self.socialmedia_creators_map[content_object]

    def get_socialmedia(self, socialmedia: str) -> Type:
        return self.socialmedias_map[socialmedia]

    def save_content_posted(self, **kwargs):
        shared_model_historial = kwargs["shared_model_historial"]
        shared_model_historial_obj = shared_model_historial._default_manager.create(
            user=User.objects.get(id=1),
            post_type=kwargs["post_type"],
            platform_shared=kwargs["socialmedia"],
            social_id=kwargs["social_id"],
            title=kwargs["title"],
            content=kwargs["content"],
            default_title=kwargs.get("default_title"),
            default_content=kwargs.get("default_content"),
            extra_description=kwargs.get("extra_description"),
            metadata=kwargs.get("metadata"),
        )

        title_emojis = kwargs.get("title_emojis", [])
        hashtags = kwargs.get("hashtags", [])
        if title_emojis:
            shared_model_historial_obj.title_emojis.add(*title_emojis)
        if hashtags:
            shared_model_historial_obj.hashtags.add(*hashtags)

    def share_content(self, socialmedia_list: List[str], content_object: int):
        socialmedia_content_creator = self.get_creator(content_object)
        socialmedia_content = socialmedia_content_creator().create_social_media_content_from_object()
        title = socialmedia_content["title"]["title"]
        content = socialmedia_content["content"]["content"]
        default_title = socialmedia_content["title"].get("default_title")
        default_content = socialmedia_content["content"].get("default_content")
        link = socialmedia_content["link"]
        media = socialmedia_content["media"]
        content_shared = socialmedia_content["content_shared"]
        shared_model_historial = socialmedia_content["shared_model_historial"]
        hashtags_list = socialmedia_content["hashtags_list"]
        hashtags = socialmedia_content["hashtags"]

        for socialmedia in socialmedia_list:
            socialmedia_obj = self.get_socialmedia(socialmedia)
            socialmedia_obj_response = socialmedia_obj().post()
