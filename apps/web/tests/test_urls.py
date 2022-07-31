import vcr
from model_bakery import baker

from django.test import TestCase

from apps.web.urls import (
)

web_vcr = vcr.VCR(
    cassette_library_dir='cassettes/web/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

