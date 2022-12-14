from unittest import skip

from django.conf import settings
from django.test import TestCase, override_settings

import vcr

from src.content_creation.constants import POST_TYPE_TEXT
from src.socialmedias.outils.socialposter.facepy import Facebook
from src.socialmedias import constants

facebook_vcr = vcr.VCR(
    cassette_library_dir="cassettes/facebook/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
    filter_post_data_parameters=["access_token"],
)


@override_settings(FACEBOOK_APP_ID="app-id")
class TestFacePoster(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.facebook = Facebook(
            settings.TEST_FACEBOOK_ID,
            settings.TEST_FB_PAGE_ACCESS_TOKEN,
            "Inversiones.y.Finanzas.Para.Todos.Tests",
        )
        cls.facebook_old = Facebook(
            settings.TEST_FACEBOOK_ID,
            settings.TEST_FB_PAGE_ACCESS_TOKEN,
            "Inversiones.y.Finanzas.Para.Todos.Tests",
            is_old_page=True,
        )

    def test_create_fb_description(self):
        description = self.facebook.create_fb_description("contenido", "#list #de #hashtags", "enlace")
        assert (
            """contenido

        Descubre el resto en: enlace
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
        #list #de #hashtags
        """
            == description
        )

    def test_build_base_url(self):
        assert "https://graph.facebook.com/v15.0/" == self.facebook_old.build_base_url()
        assert "https://graph-video.facebook.com/v15.0/" == self.facebook_old.build_base_url(is_video=True)
        assert "https://graph.facebook.com/v15.0/105836681984738/" == self.facebook.build_base_url()

    def test_build_action_url_auth(self):
        assert "https://graph.facebook.com/v15.0/oauth/access_token" == self.facebook_old.build_action_url(
            constants.FACEBOOK_OAUTH_ACCESS_TOKEN
        )
        assert "https://graph.facebook.com/v15.0/105836681984738/oauth/access_token" == self.facebook.build_action_url(
            constants.FACEBOOK_OAUTH_ACCESS_TOKEN
        )

    def test_build_action_url_text(self):
        assert "https://graph.facebook.com/v15.0/feed" == self.facebook_old.build_action_url(
            constants.FACEBOOK_POST_TEXT_PAGE
        )
        assert "https://graph.facebook.com/v15.0/105836681984738/feed" == self.facebook.build_action_url(
            constants.FACEBOOK_POST_TEXT_PAGE
        )

    def test_build_action_url_video(self):
        assert "https://graph-video.facebook.com/v15.0/videos" == self.facebook_old.build_action_url(
            constants.FACEBOOK_POST_VIDEO_PAGE
        )
        assert "https://graph-video.facebook.com/v15.0/105836681984738/videos" == self.facebook.build_action_url(
            constants.FACEBOOK_POST_VIDEO_PAGE
        )

    def test_build_action_url_image(self):
        assert "https://graph.facebook.com/v15.0/photos" == self.facebook_old.build_action_url(
            constants.FACEBOOK_POST_IMAGE_PAGE
        )
        assert "https://graph.facebook.com/v15.0/105836681984738/photos" == self.facebook.build_action_url(
            constants.FACEBOOK_POST_IMAGE_PAGE
        )

    def test_build_auth_url(self):
        redirect_url = "redirect_uri=https://inversionesyfinanzas.xyz/facebook-auth/"
        base_path = "https://www.facebook.com/v15.0/dialog/oauth?"
        params = f"client_id=app-id&{redirect_url}&state=InvFin&auth_type=rerequest"
        assert f"{base_path}{params}" == self.facebook.build_auth_url()

    @skip("not ready")
    def test_post(self):
        post_content = dict(
            media="",
            title="Default title",
            content="Default content",
            hashtags="#default #hashtags",
            post_type=POST_TYPE_TEXT,
            link="enlace",
        )
        fb_response = self.facebook.post(**post_content)
        print(fb_response)
        expected_content = """Default content

        Descubre el resto en: enlace
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
        #default #hashtags
        """
        expected_response = {
            "post_response": [
                {
                    "social_id": "",
                    "title": "Default title",
                    "content": expected_content,
                    "post_type": POST_TYPE_TEXT,
                    "use_hashtags": True,
                    "use_emojis": True,
                    "use_link": True,
                    "use_default_title": True,
                    "use_default_content": True,
                }
            ]
        }
        assert expected_response == fb_response

    @skip("Not ready")
    def test_get_long_live_page_token(self):
        fb_response = self.facebook.get_long_live_page_token()
        print(fb_response)
