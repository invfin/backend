import vcr
from model_bakery import baker

from django.test import TestCase

from apps.screener.urls import (
)

screener_vcr = vcr.VCR(
    cassette_library_dir='cassettes/screener/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

