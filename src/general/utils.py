import binascii
import csv
import functools
import json
import os
import random
from typing import Optional, Type
from urllib.parse import urlunparse

from django.conf import settings
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.defaultfilters import slugify
from django.urls import reverse as simple_reverse

from src.public_blog.models import WriterProfile

from .constants import BUSINESS_SUBDOMAIN

User = get_user_model()
FULL_DOMAIN = settings.FULL_DOMAIN


def add_new_default_check(checking, json_file):
    with open(json_file, "r") as read_checks_json:
        checks_json = json.load(read_checks_json)
    checks_json.update({f"has_{checking}": {"state": "no", "time": ""}})
    with open(json_file, "w") as writte_checks_json:
        json.dump(checks_json, writte_checks_json, indent=2, separators=(",", ": "))


class ChartSerializer:
    @staticmethod
    def generate_json(
        comparing_json: dict, items: Optional[list] = None, chart_type: str = "line"
    ) -> dict:
        labels = comparing_json["labels"]
        chart_data = {"labels": labels, "fields": []}
        if not items:
            items = list(range(len(comparing_json["fields"])))

        for field in [comparing_json["fields"][num] for num in items]:
            chart_data["fields"].append(
                {
                    "label": field["title"],
                    "data": field["values"],
                    "backgroundColor": "",
                    "borderColor": "",
                    "yAxisID": "right",
                    "order": 0,
                    "type": chart_type,
                }
            )

        return chart_data

    def generate_portfolio_charts(self):
        return {
            "labels": [],
            "datasets": [
                {
                    "label": "",
                    "data": 0,
                    "backgroundColor": "#" + "".join(
                        [random.choice("ABCDEF0123456789") for _ in range(6)]
                    ),
                }
            ],
        }


class ExportCsv:
    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        meta = f"{meta}".replace(".", "-")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={meta}.csv"
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export to csv"


class UniqueCreator:
    @classmethod
    def create_unique_field(cls, model, value, field, original_value="", extra: int = 0):
        if model.__class__.objects.filter(**{field: value}).exists():
            if field == "key":
                value = UniqueCreator.generate_key()
            else:
                value = UniqueCreator.generate_slug(original_value, extra)
            return UniqueCreator.create_unique_field(model, value, field)
        return value

    @classmethod
    def generate_key(cls):
        return binascii.hexlify(os.urandom(20)).decode()

    @classmethod
    def generate_slug(cls, value="", extra: int = 0):
        extra += 1
        return slugify(value + str(extra))


class HostChecker:
    def __init__(self, request) -> None:
        self.request = request
        self.host = self.get_host()
        self.urlconf = "src.public_blog.urls"
        #: :func:`reverse` bound to insecure (non-HTTPS) URLs scheme
        self.insecure_reverse = functools.partial(self.reverse, scheme="http")

        #: :func:`reverse` bound to secure (HTTPS) URLs scheme
        self.secure_reverse = functools.partial(self.reverse, scheme="https")

        #: :func:`reverse` bound to be relative to the current scheme
        self.relative_reverse = functools.partial(self.reverse, scheme="")

    def get_host(self) -> str:
        return self.request.get_host().split(".")[0]

    def host_is_business(self) -> bool:
        return self.host == BUSINESS_SUBDOMAIN

    def get_writer(self) -> Optional[WriterProfile]:
        return WriterProfile.objects.filter(host_name=self.host).first()

    def return_user_writer(self) -> Optional[Type]:
        writer = self.get_writer()
        return writer.user if writer else None

    def current_site_domain(self):
        domain = settings.CURRENT_DOMAIN

        prefix = "www."
        if getattr(settings, "REMOVE_WWW_FROM_DOMAIN", False) and domain.startswith(prefix):
            domain = domain.replace(prefix, "", 1)

        return domain

    def urljoin(self, domain, path=None, scheme=None):
        """
        Joins a domain, path and scheme part together, returning a full URL.
        :param domain: the domain, e.g. ``example.com``
        :param path: the path part of the URL, e.g. ``/example/``
        :param scheme: the scheme part of the URL, e.g. ``http``, defaulting to the
            value of ``settings.DEFAULT_URL_SCHEME``
        :returns: a full URL
        """
        if scheme is None:
            scheme = getattr(settings, "DEFAULT_URL_SCHEME", "http")

        return urlunparse((scheme, domain, path or "", None, None, None))

    def reverse(
        self, viewname, subdomain=None, scheme=None, args=None, kwargs=None, current_app=None
    ):
        """
        Reverses a URL from the given parameters, in a similar fashion to
        :meth:`django.core.urlresolvers.reverse`.
        :param viewname: the name of URL
        :param subdomain: the subdomain to use for URL reversing
        :param scheme: the scheme to use when generating the full URL
        :param args: positional arguments used for URL reversing
        :param kwargs: named arguments used for URL reversing
        :param current_app: hint for the currently executing application
        """
        urlconf = settings.SUBDOMAIN_URLCONFS.get(subdomain, settings.ROOT_URLCONF)

        domain = self.current_site_domain()
        if subdomain is not None:
            domain = "%s.%s" % (subdomain, domain)

        path = simple_reverse(
            viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
        )
        return self.urljoin(domain, path, scheme=scheme)
