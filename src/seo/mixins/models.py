from django.conf import settings


class SeoMetaMixin:
    @property
    def schema_org(self):
        if self.object_name == "Question":  # type: ignore
            schema_org = self.schema_org
        else:
            meta_url = f"{FULL_DOMAIN}/definicion/{self.slug}/"  # type: ignore
            if self.object_name == "PublicBlog":  # type: ignore
                meta_url = f"{self.author.custom_url}/p/{self.slug}/"  # type: ignore
            schema_org = {
                "@context": "https://schema.org",
                "@type": "Article",
                "mainEntityOfPage": {"@type": "WebPage", "@id": f"{meta_url}"},
                "headline": f"{self.title}",  # type: ignore
                "image": f"{self.non_thumbnail_url}",  # type: ignore
                "datePublished": f"{self.published_at}",  # type: ignore
                "author": {"@type": "Person", "name": f"{self.author.full_name}"},  # type: ignore
                "publisher": {
                    "@type": "Organization",
                    "name": "Inversiones & Finanzas",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{settings.FULL_DOMAIN}/static/general/assets/img/favicon/favicon.ico",
                    },
                },
            }
        return schema_org
