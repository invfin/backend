from django.conf import settings
from django.core.management import BaseCommand

from pyfacebook import GraphAPI
import requests

from src.socialmedias import constants
from src.socialmedias.outils.socialposter.facepy import Facebook


class Command(BaseCommand):
    def handle(self, *args, **options):
        post_content = dict(
            media="",
            title="Default title",
            content="Default content #default #hashtags",
            hashtags="",
            post_type=3,
            link="https://inversionesyfinanzas.xyz",
        )
        fb_response = Facebook(
            settings.ACTUAL_FACEBOOK_ID,
            settings.ACTUAL_FB_PAGE_ACCESS_TOKEN,
            facebook_page_name="Inversiones.y.Finanzas.Para.Todos.Tests",
        ).post(**post_content)
        print(fb_response)
