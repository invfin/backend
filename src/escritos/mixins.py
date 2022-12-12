from django.conf import settings

from bs4 import BeautifulSoup as bs

FULL_DOMAIN = settings.FULL_DOMAIN


class BaseEscritosMixins:
    def search_image(self, content):
        soup = bs(content, "html.parser")
        images = [img for img in soup.find_all("img")]
        image = False
        if len(images) != 0:
            image = images[0]
            image = image.get("src")
        return image

    def extra_info(self, image):
        if image is False:
            self.in_text_image = False
        else:
            self.in_text_image = True
            self.non_thumbnail_url = image

    def create_meta_information(self, type_content):
        from src.seo.models import MetaParameters, MetaParametersHistorial

        meta_url = f"{FULL_DOMAIN}/definicion/{self.slug}/"
        if type_content == "blog":
            meta_url = f"{self.author.custom_url}/p/{self.slug}/"

        meta = MetaParameters.objects.create(
            meta_title=self.title,
            meta_description=self.resume,
            meta_img=self.non_thumbnail_url,
            meta_url=meta_url,
            meta_keywords=", ".join([tag.name for tag in self.tags.all()]),
            meta_author=self.author,
            published_time=self.published_at,
            modified_time=self.updated_at,
            created_at=self.created_at,
            schema_org={
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{meta_url}"},
                "headline": f"{self.title}",
                "image": f"{self.non_thumbnail_url}",
                "datePublished": f"{self.published_at}",
                "author": {"@type": "Person", "name": f"{self.author.full_name}"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Inversiones & Finanzas",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico",
                    },
                },
            },
        )
        meta_historial = MetaParametersHistorial.objects.create(
            parameter_settings=meta,
            in_use=True,
        )

        self.meta_information = meta_historial

    def save_secondary_info(self, content_type):
        if content_type != "blog":
            for term_part in self.term_parts.all():
                image = self.search_image(term_part.content)
                if image != False:
                    break
        else:
            image = self.search_image(self.content)
        self.extra_info(image)
        self.create_meta_information(content_type)
