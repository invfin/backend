import vcr
from model_bakery import baker

from django.test import TestCase

from apps.recsys.urls import (
)

recsys_vcr = vcr.VCR(
    cassette_library_dir='cassettes/recsys/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

