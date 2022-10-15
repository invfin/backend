import datetime

import requests
from django.conf import settings

from apps.socialmedias.constants import FACEBOOK_GRAPH_URL, FACEBOOK_GRAPH_VIDEO_URL


class Facebook:
    def __init__(self, page_id: str, page_access_token: str, facebook_page_name: str) -> None:
        self.page_id = page_id
        self.facebook_page_name = facebook_page_name
        self.app_secret = settings.FACEBOOK_APP_SECRET
        self.long_lived_user_token = settings.FB_USER_ACCESS_TOKEN
        self.page_access_token = page_access_token
        self.post_facebook_url = f"{FACEBOOK_GRAPH_URL}{self.page_id}"
        self.post_facebook_video_url = f"{FACEBOOK_GRAPH_VIDEO_URL}{self.page_id}"

    def get_long_live_user_token(self, app_id, user_token):
        url = f"{FACEBOOK_GRAPH_URL}oauth/access_token"

        parameters = {
            "grant_type": "fb_exchange_token",
            "client_id": app_id,
            "client_secret": self.app_secret,
            "fb_exchange_token": user_token,
        }

        re = requests.get(url, params=parameters)

        # if re.status_code == 200:
        #     token = str(re.json()['access_token'])
        #     FB_USER_ACCESS_TOKEN
        #     return token

    def get_long_live_page_token(self, old=False):
        parameters = {"fields": "access_token", "access_token": self.long_lived_user_token}

        re = requests.get(self.post_facebook_url, params=parameters)

        # if re.status_code == 200:
        #     token = str(re.json()['access_token'])
        #     if old is False:
        #         NEW_FB_PAGE_ACCESS_TOKEN
        #     else:
        #         OLD_FB_PAGE_ACCESS_TOKEN
        #     return token

    def post_fb_video(self, video_url="", description="", title="", post_time=datetime.datetime.now(), post_now=False):
        """
        Post_now is False if the post has to be scheduled, True to post it now
        """
        files = {"source": open(video_url, "rb")}
        access_token = self.page_access_token

        data = {"access_token": access_token, "title": title, "description": description}

        if post_now is False:
            data.update({"published": False, "scheduled_publish_time": post_time})

        return self._send_content("video", data, files)

    def post_text(self, text="", post_time=datetime.datetime.now(), post_now=True, link=None, title=""):
        if post_now is False:
            pass
        else:
            data = {"access_token": self.page_access_token, "message": text, "title": title}

        if link:
            data["link"] = link

        return self._send_content("text", data)

    def post_image(self, description="", photo_url="", title="", post_time=datetime.datetime.now(), post_now=False):
        data = {"access_token": self.page_access_token, "url": photo_url}
        return self._send_content("image", data)

    def _send_content(self, content_type: str, content, files=None):
        if content_type == "video":
            re = requests.post(f"{self.post_facebook_video_url}/videos", files=files, data=content)
        elif content_type == "text":
            re = requests.post(f"{self.post_facebook_url}/feed", data=content)
        elif content_type == "image":
            re = requests.post(f"{self.post_facebook_url}/photos", data=content)

        response = {}
        json_re = re.json()
        if re.status_code == 200:
            response["result"] = "success"
            response["extra"] = str(json_re["id"])

        elif json_re["error"]["code"] == 190:
            # logger.error(f'{json_re}, Need new user token')
            response["result"] = "error"
            response["where"] = "send content facebook"
            response["message"] = "Need new user token"

        else:
            # logger.error(f'{json_re}')
            response["result"] = "error"
            response["where"] = "send content facebook"
            response["message"] = f"{json_re}"

        return response

    def post_on_facebook(
        self, title: str, description: str = None, post_type: int = 3, link: str = None, media_url: str = None, **kwargs
    ):
        platform = "facebook"

        description = self.create_fb_description(
            description=description, link=link, hashtags=[hashtag.title for hashtag in hashtags]
        )

        if post_type == 1 or post_type == 5 or post_type == 7:
            content_type = "video"
            video_url = ""
            post_response = self.post_fb_video(
                video_url=video_url, description=description, title=custom_title, post_now=True
            )

        elif post_type == 2 or post_type == 6:
            content_type = "image"
            post_response = self.post_image()

        elif post_type == 3 or post_type == 4:
            content_type = "text"
            description = f"{description}"

            post_response = self.post_text(text=description, link=link, title=title)

        if post_response["result"] == "success":
            return {
                "post_type": post_type,
                "social_id": post_response["extra"],
                "title": custom_title,
                "description": description,
                "platform_shared": platform,
            }
        else:
            return self.post_on_facebook(title, description, num_emojis, post_type, link, media_url)

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

    def create_fb_description(self, description: str, link: str = "", hashtags: str = ""):
        return f"""{description}

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
