import vcr
from model_bakery import baker

from django.test import TestCase

from apps.escritos.urls import (
)

escritos_vcr = vcr.VCR(
    cassette_library_dir='cassettes/escritos/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

