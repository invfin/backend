import vcr
from model_bakery import baker

from django.test import TestCase

from apps.roboadvisor.urls import (
)

roboadvisor_vcr = vcr.VCR(
    cassette_library_dir='cassettes/roboadvisor/urls/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)

