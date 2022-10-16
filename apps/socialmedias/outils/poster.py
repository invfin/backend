import random
from typing import List, Dict, Type

from django.conf import settings
from django.contrib.auth import get_user_model


from apps.socialmedias.socialposter.facepy import Facebook
from apps.socialmedias.socialposter.tweetpy import Twitter
from apps.socialmedias.outils.content_creation import (
    CompanyContentCreation,
    CompanyNewsContentCreation,
    TermContentCreation,
    QuestionContentCreation,
    PublicBlogContentCreation,
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
    content_creators_map: Dict = {
        constants.QUESTION: QuestionContentCreation,
        constants.NEWS: CompanyNewsContentCreation,
        constants.TERM: TermContentCreation,
        constants.PUBLIC_BLOG: PublicBlogContentCreation,
        constants.COMPANY: CompanyContentCreation,
    }

    def get_creator(self, content_object: int) -> Type:
        return self.content_creators_map[content_object]

    def get_socialmedia(self, socialmedia: str) -> Type:
        return self.socialmedias_map[socialmedia]

    def prepare_data_to_be_saved(
        self,
        socialmedia_post_response: Dict,
        platform_shared: str,
        link: str,
        socialmedia_content: Dict,
    ) -> Dict:
        response_dict = dict(
            post_type=socialmedia_post_response["post_type"],
            platform_shared=platform_shared,
            social_id=socialmedia_post_response["social_id"],
            title=socialmedia_post_response.get("title", ""),
            content=socialmedia_post_response["content"],
        )
        if socialmedia_post_response["use_hashtags"]:
            response_dict["link"] = socialmedia_content["hashtags_list"]
        if socialmedia_post_response["use_emojis"]:
            response_dict["title_emojis"] = socialmedia_content["title"].get("title_emojis", [])
        if socialmedia_post_response["use_link"]:
            response_dict["link"] = link
        if socialmedia_post_response["use_default_title"]:
            response_dict["default_title"] = socialmedia_content["title"].get("default_title")
        if socialmedia_post_response["use_default_content"]:
            response_dict["default_content"] = socialmedia_content["content"].get("default_content")
        return response_dict

    def save_content_posted(self, **kwargs):
        shared_model_historial = kwargs.pop("shared_model_historial")
        title_emojis = kwargs.pop("title_emojis", [])
        hashtags_list = kwargs.pop("hashtags_list", [])

        shared_model_historial_obj = shared_model_historial._default_manager.create(
            user=User.objects.get(id=1),
            post_type=kwargs["post_type"],
            platform_shared=kwargs["platform_shared"],
            social_id=kwargs["social_id"],
            title=kwargs["title"],
            content=kwargs["content"],
            default_title=kwargs.get("default_title"),
            default_content=kwargs.get("default_content"),
            extra_description=kwargs.get("extra_description"),
            metadata=kwargs.get("metadata"),
        )

        if title_emojis:
            shared_model_historial_obj.title_emojis.add(*title_emojis)
        if hashtags_list:
            shared_model_historial_obj.hashtags.add(*hashtags_list)

    def share_content(self, content_object: int, socialmedia_list: List[Dict]):
        socialmedia_content_creator = self.get_creator(content_object)
        socialmedia_content = socialmedia_content_creator().create_social_media_content_from_object()

        title = socialmedia_content["title"]["title"]
        content = socialmedia_content["content"]["content"]
        link = socialmedia_content["link"]
        media = socialmedia_content.get("media", "")

        for platform_post_type_dict in socialmedia_list:
            post_type = platform_post_type_dict["post_type"]
            if not media and post_type != constants.POST_TYPE_TEXT:
                post_type = constants.POST_TYPE_TEXT
            platform_shared = platform_post_type_dict["platform_shared"]

            socialmedia_obj = self.get_socialmedia(platform_shared)
            socialmedia_obj_response = socialmedia_obj().post(
                title=title,
                content=content,
                media=media,
                hashtags=socialmedia_content["hashtags"],
                link=link,
            )
            for socialmedia_post_response in socialmedia_obj_response["post_response"]:
                response_dict = self.prepare_data_to_be_saved(
                    socialmedia_post_response,
                    platform_shared,
                    link,
                    socialmedia_content,
                )
                self.save_content_posted(
                    content_shared=socialmedia_content["content_shared"],
                    shared_model_historial=socialmedia_content["shared_model_historial"],
                    **response_dict,
                )
