import vcr

from django.test import TestCase

from unittest import skip
from bfet import DjangoTestingModel

from apps.empresas.parse.others.yahoo_finance import ParseYahooFinance


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/yahoo_finance/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("Don't wnat to test")
class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()
