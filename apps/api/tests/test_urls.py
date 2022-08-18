import vcr
from model_bakery import baker

from django.test import TestCase

from apps.api.urls import (
)

api_vcr = vcr.VCR(
    cassette_library_dir='cassettes/api/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

