import datetime
from typing import Dict

import requests
from django.conf import settings

from src.socialmedias import constants


class Facebook:
    def __init__(self, page_id: str, page_access_token: str, facebook_page_name: str) -> None:
        self.page_id = page_id
        self.facebook_page_name = facebook_page_name
        self.app_secret = settings.FACEBOOK_APP_SECRET
        self.long_lived_user_token = settings.FB_USER_ACCESS_TOKEN
        self.page_access_token = page_access_token
        self.post_facebook_url = f"{constants.FACEBOOK_GRAPH_URL}{self.page_id}"
        self.post_facebook_video_url = f"{constants.FACEBOOK_GRAPH_VIDEO_URL}{self.page_id}"

    def handle_responses(self, response: requests.Response, field_to_retrieve: str) -> Dict:
        response_result = {}
        response_dict = response.json()
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

    def get_long_live_user_token(self, app_id, user_token):
        """method to get a token if a response is 403

        Parameters
        ----------
            app_id : _type_
                _description_

            user_token : _type_
                _description_

        Returns
        -------
            str
                returns a FB_USER_ACCESS_TOKEN
        """

        url = f"{constants.FACEBOOK_GRAPH_URL}oauth/access_token"

        parameters = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": user_token,
        }

        response = requests.get(url, params=parameters)

        return self.handle_responses(response, "access_token")

    def get_long_live_page_token(self):
        """Method to get a NEW_FB_PAGE_ACCESS_TOKEN

        Returns
        -------
            str
                NEW_FB_PAGE_ACCESS_TOKEN
        """
        parameters = {"fields": "access_token", "access_token": self.long_lived_user_token}

        response = requests.get(self.post_facebook_url, params=parameters)
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
        if not kwargs["post_now"]:
            content.update({"published": False, "scheduled_publish_time": kwargs["scheduled_publish_time"]})
        content.update({"access_token": self.page_access_token})
        if content_type == "video":
            files = {"source": open(kwargs["media_url"], "rb")}
            response = requests.post(f"{self.post_facebook_video_url}/videos", data=content, files=files)

        elif content_type == "text":
            content.update({"link": kwargs["link"]})
            response = requests.post(f"{self.post_facebook_url}/feed", data=content)

        else:
            content.update({"url": kwargs["media_url"]})
            response = requests.post(f"{self.post_facebook_url}/photos", data=content)

        return self.handle_responses(response, "id")

    def post(self, **kwargs):
        media_url = kwargs.get("media", "")
        scheduled_publish_time = kwargs.get("scheduled_publish_time", "")
        post_type = kwargs["post_type"]
        post_now = kwargs.get("post_now", True)
        title = kwargs["title"]
        link = kwargs["link"]

        content = self.create_fb_description(kwargs["content"], kwargs["hashtags"], link)
        data = {"title": title, "description": content}

        if post_type == constants.POST_TYPE_TEXT or post_type == constants.POST_TYPE_REPOST:
            content_type = "text"
        elif post_type == constants.POST_TYPE_IMAGE or post_type == constants.POST_TYPE_TEXT_IMAGE:
            content_type = "image"
        else:
            content_type = "video"

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
