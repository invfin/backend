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
    facebook_poster: Facebook = Facebook(
        settings.NEW_FACEBOOK_ID,
        settings.NEW_FB_PAGE_ACCESS_TOKEN,
        "InversionesyFinanzas",
    )
    twitter_poster: Twitter = Twitter(
        settings.TWITTER_CONSUMER_KEY,
        settings.TWITTER_CONSUMER_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET,
    )
    social_media_creators = {
        constants.QUESTION: QuestionContentCreation,
        constants.NEWS: CompanyNewsContentCreation,
        constants.TERM: TermContentCreation,
        constants.PUBLIC_BLOG: PublicBlogContentCreation,
        constants.COMPANY: CompanyContentCreation,
    }
    # instagram_poster
    # youtube_poster

    def question_content(self):
        pass

    def news_content(self):
        pass

    def term_content(self):
        pass

    def publicblog_content(self):
        pass

    def company_content(self):
        pass

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

    def share_content(self, model_for_social_medias_content: int, social_medias: List, specific_model: Model = None):
        social_media_content_from_obj = social_media_content[model_for_social_medias_content]
        content_for_social_media = social_media_content_from_obj(specific_model)
        content_generated_and_posted = self.generate_content(social_medias, content_for_social_media)
        shared_model_historial = content_for_social_media.pop("shared_model_historial")
        self.save_post(content_generated_and_posted, shared_model_historial)
