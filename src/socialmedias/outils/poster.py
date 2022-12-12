from typing import Dict, List, Type

from django.conf import settings
from django.contrib.auth import get_user_model

from src.content_creation import constants as content_creation_constants
from src.content_creation.outils.content_creator import (
    CompanyContentCreation,
    CompanyNewsContentCreation,
    PublicBlogContentCreation,
    QuestionContentCreation,
    TermContentCreation,
)
from src.socialmedias import constants
from src.socialmedias.outils.socialposter.facepy import Facebook
from src.socialmedias.outils.socialposter.tweetpy import Twitter

User = get_user_model()


class SocialPosting:
    facebook: Facebook = Facebook(
        settings.OLD_FACEBOOK_ID,
        settings.OLD_FB_PAGE_ACCESS_TOKEN,
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
        constants.INSTAGRAM: instagram,
        constants.YOUTUBE: youtube,
        constants.REDDIT: "",
        constants.WHATSAPP: "",
        constants.LINKEDIN: "",
        constants.PINTEREST: "",
        constants.TUMBLR: "",
    }
    content_creators_map: Dict = {
        content_creation_constants.QUESTION_FOR_CONTENT: QuestionContentCreation,
        content_creation_constants.NEWS_FOR_CONTENT: CompanyNewsContentCreation,
        content_creation_constants.TERM_FOR_CONTENT: TermContentCreation,
        content_creation_constants.PUBLIC_BLOG_FOR_CONTENT: PublicBlogContentCreation,
        content_creation_constants.COMPANY_FOR_CONTENT: CompanyContentCreation,
    }

    def get_creator(self, content_object: str) -> Type:
        return self.content_creators_map[content_object]

    def get_socialmedia(self, socialmedia: str) -> Type:
        return self.socialmedias_map[socialmedia]

    def prepare_data_to_be_saved(
        self,
        socialmedia_post_response: Dict,
        socialmedia_content: Dict,
    ) -> Dict:
        response_dict = dict(
            post_type=socialmedia_post_response["post_type"],
            platform_shared=socialmedia_post_response["platform_shared"],
            social_id=socialmedia_post_response["social_id"],
            title=socialmedia_post_response.get("title", ""),
            content=socialmedia_post_response["content"],
        )
        if socialmedia_post_response["use_hashtags"]:
            response_dict["hashtags_list"] = socialmedia_content["hashtags_list"]
        if socialmedia_post_response["use_emojis"]:
            response_dict["title_emojis"] = socialmedia_content.get("title_emojis", [])
        # if socialmedia_post_response["use_link"]:
        #     response_dict["link"] = socialmedia_content["link"]
        if socialmedia_post_response["use_default_title"]:
            response_dict["default_title"] = socialmedia_content.get("default_title", None)
        if socialmedia_post_response["use_default_content"]:
            response_dict["default_content"] = socialmedia_content.get("default_content", None)
        return response_dict

    def save_content_posted(self, **kwargs):
        shared_model_historial = kwargs.pop("shared_model_historial")
        title_emojis = kwargs.pop("title_emojis", [])
        hashtags_list = kwargs.pop("hashtags_list", [])

        shared_model_historial_obj = shared_model_historial._default_manager.create(
            user=User.objects.get(id=1), **kwargs
        )

        if title_emojis:
            shared_model_historial_obj.title_emojis.add(*title_emojis)
        if hashtags_list:
            shared_model_historial_obj.hashtags.add(*hashtags_list)

    def share_content(self, content_object: str, socialmedia_list: List[Dict]):
        """The main method that get the content crator according to the model, then it gets
        the socialmedia and post on it. Once the post has been successfull it saves the results.
        For the moment it'll probably be most used from tasks.

        Parameters
        ----------
            content_object : str
                A string from constants that will indicate which model to use to get an obj for the content
                Example: constants.COMPANY_FOR_CONTENT

            socialmedia_list : List[Dict]
                A list of dicts with the socialmedia platform to post and the post type.
                Example: {"platform_shared": constants.FACEBOOK, "post_type": constants.POST_TYPE_TEXT_IMAGE}
        """
        socialmedia_content_creator = self.get_creator(content_object)
        for platform_post_type_dict in socialmedia_list:
            platform_shared = platform_post_type_dict["platform_shared"]
            socialmedia_content = socialmedia_content_creator(platform_shared).create_social_media_content_from_object()
            media = socialmedia_content.get("media", "")
            post_type = platform_post_type_dict["post_type"]
            if not media and post_type != content_creation_constants.POST_TYPE_TEXT:
                post_type = content_creation_constants.POST_TYPE_TEXT
            # Here is where we are posting on socilamedia
            socialmedia_obj = self.get_socialmedia(platform_shared)
            socialmedia_obj_response = socialmedia_obj.post(
                **socialmedia_content,
                post_type=post_type,
            )
            # Here we get the response and save it
            for socialmedia_post_response in socialmedia_obj_response["post_response"]:
                response_dict = self.prepare_data_to_be_saved(
                    socialmedia_post_response,
                    socialmedia_content,
                )
                self.save_content_posted(
                    content_shared=socialmedia_content["content_shared"],
                    shared_model_historial=socialmedia_content["shared_model_historial"],
                    **response_dict,
                )
