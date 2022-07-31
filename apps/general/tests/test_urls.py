import vcr
from model_bakery import baker

from django.test import TestCase

from apps.general.urls import (
)

general_vcr = vcr.VCR(
    cassette_library_dir='cassettes/general/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

