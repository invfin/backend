from typing import Dict
import urllib.parse

from django.conf import settings

from pyfacebook import GraphAPI
import requests

from src.content_creation import constants as content_creation_constants
from src.socialmedias import constants


class Facebook:
    redirect_uri = "https://inversionesyfinanzas.xyz/facebook-auth/"
    state = "InvFin"

    def __init__(
        self,
        page_id: str,
        page_access_token: str,
        facebook_page_name: str,
        is_old_page: bool = False,
    ) -> None:
        self.page_id = page_id
        self.facebook_page_name = facebook_page_name
        self.page_access_token = page_access_token
        self.is_old_page = is_old_page

    @staticmethod
    def authorisation_url():
        api = GraphAPI(app_id=settings.FACEBOOK_APP_ID, app_secret=settings.FACEBOOK_APP_SECRET, oauth_flow=True)
        authorization_url, state = api.get_authorization_url(
            redirect_uri="https://inversionesyfinanzas.xyz/",
            # state="InvFin",
        )
        return authorization_url

    def build_base_url(
        self,
        version: str = constants.FACEBOOK_GRAPH_API_VERSION,
        is_video: bool = False,
        is_for_auth: bool = False,
    ) -> str:
        base_url = constants.FACEBOOK_GRAPH_URL
        if is_video:
            base_url = constants.FACEBOOK_GRAPH_VIDEO_URL
        base_url = f"{base_url}{version}"
        if not self.is_old_page and not is_for_auth:
            base_url = f"{base_url}/{self.page_id}/"
        return base_url

    def build_action_url(
        self,
        action: str,
        version: str = constants.FACEBOOK_GRAPH_API_VERSION,
    ) -> str:
        is_video, is_for_auth = False, False
        if action == constants.FACEBOOK_POST_VIDEO_PAGE:
            is_video = True
        if action == constants.FACEBOOK_OAUTH_ACCESS_TOKEN:
            is_for_auth = True
        base_url = self.build_base_url(version, is_video, is_for_auth)
        return f"{base_url}{action}"

    def build_auth_url(self) -> str:
        """
        https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow
        """
        base_path = "https://www.facebook.com/v15.0/dialog/oauth"
        base_params = {
            "auth_type": "rerequest",
            "client_id": {settings.FACEBOOK_APP_ID},
            "redirect_uri": {self.redirect_uri},
            "state": {self.state},
        }
        encoded_params = urllib.parse.urlencode(base_params)
        return f"{base_path}?{encoded_params}"

    @classmethod
    def change_auth_code_per_access_token(cls, code: str) -> Dict[str, str]:
        """
        https://developers.facebook.com/docs/facebook-login/guides/advanced/manual-flow
        """
        params = {
            "client_id": settings.FACEBOOK_APP_ID,
            "redirect_uri": cls.redirect_uri,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "code": code,
        }
        response = requests.get("https://graph.facebook.com/v15.0/oauth/access_token?", params=params)
        response.raise_for_status()
        return response.json()

    @classmethod
    def get_access_token_information(cls, json_response: Dict[str, str]) -> str:
        # token_type = json_response["token_type"] see what to do with that
        # expires_in = json_response["expires_in"] seems not to be in the response anymore
        return json_response["access_token"]

    @classmethod
    def return_user_access_token(cls, code: str):
        json_response = cls.change_auth_code_per_access_token(code)
        token = cls.get_access_token_information(json_response)
        return token

    def handle_responses(self, response: requests.Response, field_to_retrieve: str) -> Dict:
        response_result = {}
        response_dict = response.json()
        print(response.json())
        if response.status_code == 200:
            response_result["result"] = "success"
            response_result["extra"] = str(response_dict[field_to_retrieve])

        elif response_dict["error"]["code"] == 190:
            response_result["result"] = "error"
            response_result["where"] = "send content facebook"
            response_result["message"] = "Need new user token"

        else:
            # logger.error(f'{json_re}')
            response_result["result"] = "error"
            response_result["where"] = "send content facebook"
            response_result["message"] = f"{response_dict}"

        return response_result

    def get_long_live_user_token(self, user_token: str) -> Dict:
        url = self.build_action_url(constants.FACEBOOK_OAUTH_ACCESS_TOKEN)
        parameters = {
            "grant_type": "fb_exchange_token",
            "client_id": settings.FACEBOOK_APP_ID,
            "client_secret": settings.FACEBOOK_APP_SECRET,
            "fb_exchange_token": user_token,
        }
        response = requests.get(url, params=parameters)
        return self.handle_responses(response, "access_token")

    def get_long_live_page_token(self, long_lived_user_token: str):
        parameters = {"fields": "access_token", "access_token": long_lived_user_token}
        url = self.build_base_url()

        response = requests.get(url, params=parameters)
        return self.handle_responses(response, "access_token")

    def post_content(self, content_type: str, content: Dict, **kwargs):
        """Method to post to the Facebook API

        Parameters
        ----------
            content_type : str
                Specify if you are going to post a text alone, an image with a text or a video with a text

            content : Dict
                The basic data that it's used accross the 3 types of content (title, description/message)

        Returns
        -------
            _type_
                The facebook response inside a dict with and error message if any or success
        """
        if not kwargs["post_now"] and kwargs.get("scheduled_publish_time"):
            content.update({"published": False, "scheduled_publish_time": kwargs["scheduled_publish_time"]})
        content.update({"access_token": self.page_access_token})
        files = None
        if content_type == constants.FACEBOOK_POST_VIDEO_PAGE:
            files = {"source": open(kwargs["media_url"], "rb")}

        elif content_type == constants.FACEBOOK_POST_TEXT_PAGE:
            content.update({"link": kwargs["link"]})

        else:
            content.update({"url": kwargs["media_url"]})

        url = self.build_action_url(content_type)
        response = requests.post(url, data=content, files=files)

        return self.handle_responses(response, "id")

    def post(self, **kwargs):
        media_url = kwargs.get("media", "")
        scheduled_publish_time = kwargs.get("scheduled_publish_time", "")
        post_type = kwargs["post_type"]
        post_now = kwargs.get("post_now", True)
        title = kwargs["title"]
        link = kwargs["link"]

        content = self.create_fb_description(kwargs["content"], kwargs["hashtags"], link)
        data = {"title": title, "message": content}

        if (
            post_type == content_creation_constants.POST_TYPE_TEXT
            or post_type == content_creation_constants.POST_TYPE_REPOST
        ):
            content_type = constants.FACEBOOK_POST_TEXT_PAGE
        elif (
            post_type == content_creation_constants.POST_TYPE_IMAGE
            or post_type == content_creation_constants.POST_TYPE_TEXT_IMAGE
        ):
            content_type = constants.FACEBOOK_POST_IMAGE_PAGE
        else:
            content_type = constants.FACEBOOK_POST_VIDEO_PAGE

        post_response = self.post_content(
            content_type,
            data,
            media_url=media_url,
            post_now=post_now,
            scheduled_publish_time=scheduled_publish_time,
            link=link,
        )

        if post_response["result"] == "success":
            return {
                "post_response": [
                    {
                        "social_id": post_response["extra"],
                        "title": title,
                        "content": content,
                        "post_type": post_type,
                        "use_hashtags": True,
                        "use_emojis": True,
                        "use_link": True,
                        "use_default_title": True,
                        "use_default_content": True,
                        "platform_shared": constants.FACEBOOK,
                    }
                ]
            }
        else:
            return post_response

    # def share_facebook_post(self, post_id, yb_title):
    #     default_title = DefaultTilte.objects.random_title()
    #     url_to_share = f"https://www.facebook.com/{self.facebook_page_name}/posts/{post_id}&show_text=true"
    #     return self.post_on_facebook(
    #         post_type=4,
    #         default_title=default_title,
    #         has_default_title=True,
    #         description=f"{default_title.title} {yb_title}",
    #         link=url_to_share,
    #     )

    def create_fb_description(self, content: str, hashtags: str, link: str):
        return f"""{content}

        Descubre el resto en: {link}
        Prueba las herramientas que todo inversor inteligente necesita: https://inversionesyfinanzas.xyz

        Visita nuestras redes sociales:
        Youtube: https://www.youtube.com/c/InversionesyFinanzas/
        Facebook: https://www.facebook.com/InversionesyFinanzas/
        Instagram: https://www.instagram.com/inversiones.finanzas/
        TikTok: https://www.tiktok.com/@inversionesyfinanzas?
        Twitter : https://twitter.com/InvFinz
        LinkedIn : https://www.linkedin.com/company/inversiones-finanzas
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        .
        {hashtags}
        """
