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
