import vcr
import pytest

from unittest import skip
from bfet import DjangoTestingModel as DTM

from apps.empresas.parse.finnhub import ParseFinnhub


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/finnhub/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("Skipping")
from django.test import TestCase


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinnhub()

    @parse_vcr.use_cassette(filter_query_parameters=["token"])
    def test_(self):
        pass
