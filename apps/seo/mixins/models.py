

class SeoMetaMixin:
    @property
    def schema_org(self):
        if self.object_name == "Question":
            schema_org = self.schema_org
        else:
            meta_url = f"{FULL_DOMAIN}/definicion/{self.slug}/"
            if self.object_name == "PublicBlog":
                meta_url = f"{self.author.custom_url}/p/{self.slug}/"
            schema_org = {
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
            }
        return schema_org
