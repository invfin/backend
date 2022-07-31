import vcr
from model_bakery import baker

from django.test import TestCase

from apps.cartera.urls import (
)

cartera_vcr = vcr.VCR(
    cassette_library_dir='cassettes/cartera/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

