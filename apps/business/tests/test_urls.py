import vcr
from model_bakery import baker

from django.test import TestCase

from apps.business.urls import (
)

business_vcr = vcr.VCR(
    cassette_library_dir='cassettes/business/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

