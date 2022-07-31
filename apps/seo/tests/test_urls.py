import vcr
from model_bakery import baker

from django.test import TestCase

from apps.seo.urls import (
)

seo_vcr = vcr.VCR(
    cassette_library_dir='cassettes/seo/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

