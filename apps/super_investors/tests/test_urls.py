import vcr
from model_bakery import baker

from django.test import TestCase

from apps.super_investors.urls import (
)

super_investors_vcr = vcr.VCR(
    cassette_library_dir='cassettes/super_investors/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

