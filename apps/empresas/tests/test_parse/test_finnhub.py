import vcr

from unittest import skip

from django.test import TestCase

from apps.bfet import ExampleModel
from apps.empresas.parse.finnhub import ParseFinnhub


parse_vcr = vcr.VCR(
    cassette_library_dir='cassettes/company/parse/finnhub/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


@skip("Skipping")
class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinnhub()

    @parse_vcr.use_cassette(filter_query_parameters=['token'])
    def test_(self):
        pass
