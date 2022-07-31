import vcr
from model_bakery import baker

from django.test import TestCase

from apps.empresas.urls import (
)

empresas_vcr = vcr.VCR(
    cassette_library_dir='cassettes/empresas/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

