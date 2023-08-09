from django.core.management import BaseCommand

from src.socialmedias.outils.socialposter.facepy import Facebook


class Command(BaseCommand):
    def handle(self, *args, **options):
        dict(
            media="/static/general/assets/img/general/why-us.webp",
            title="Default title",
            content="Default content #default #hashtags",
            hashtags="",
            post_type=2,
            link="https://inversionesyfinanzas.xyz",
        )
        fb_response = Facebook(
            "",
            "",
            "Inversiones & Finanzas",
        )
        print(fb_response.post(""))
