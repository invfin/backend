from django.conf import settings
from django.contrib.sitemaps import Sitemap

from src.empresas.models import Company
from src.escritos.models import Term
from src.preguntas_respuestas.models import Question
from src.public_blog.models import PublicBlog
from src.super_investors.models import Superinvestor


class SuperinvestorSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Superinvestor.objects.all()

    def location(self, obj):
        return obj.get_absolute_url()


class PublicBlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return PublicBlog.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.custom_url

    def _urls(self, page, protocol, domain):
        urls = []
        latest_lastmod = None
        all_items_lastmod = True  # track if all items have a lastmod

        paginator_page = self.paginator.page(page)
        for item in paginator_page.object_list:
            loc = self._location(item)
            priority = self._get("priority", item)
            lastmod = self._get("lastmod", item)

            if all_items_lastmod:
                all_items_lastmod = lastmod is not None
                if all_items_lastmod and (latest_lastmod is None or lastmod > latest_lastmod):
                    latest_lastmod = lastmod

            url_info = {
                "item": item,
                "location": loc,
                "lastmod": lastmod,
                "changefreq": self._get("changefreq", item),
                "priority": str(priority if priority is not None else ""),
                "alternates": [],
            }

            if self.i18n and self.alternates:
                for lang_code in self._languages():
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": lang_code,
                        }
                    )
                if self.x_default:
                    lang_code = settings.LANGUAGE_CODE
                    loc = f"{protocol}://{domain}{self._location(item, lang_code)}"
                    loc = loc.replace(f"/{lang_code}/", "/", 1)
                    url_info["alternates"].append(
                        {
                            "location": loc,
                            "lang_code": "x-default",
                        }
                    )

            urls.append(url_info)

        if all_items_lastmod and latest_lastmod:
            self.latest_lastmod = latest_lastmod

        return urls


class TermSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Term.objects.filter(status=1)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()


class CompanySitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Company.objects.filter(
            no_incs=False,
            no_bs=False,
            no_cfs=False,
        )

    def location(self, obj):
        return obj.get_absolute_url()


class QuestionSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8
    protocol = "https"

    def items(self):
        return Question.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return obj.get_absolute_url()
