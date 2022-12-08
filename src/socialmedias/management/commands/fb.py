from django.core.management import BaseCommand
from django.conf import settings
from src.socialmedias.outils.socialposter.facepy import Facebook
from src.socialmedias import constants


class Command(BaseCommand):
    def handle(self, *args, **options):
        facebook = Facebook(
            settings.TEST_FACEBOOK_ID,
            settings.TEST_FB_PAGE_ACCESS_TOKEN,
            "Inversiones.y.Finanzas.Para.Todos.Tests",
        )
        post_content = dict(
            media="",
            title="Default title",
            content="Default content",
            hashtags="#default #hashtags",
            post_type=3,
            link="enlace",
        )
        fb_response = facebook.post(**post_content)
        print(fb_response)
