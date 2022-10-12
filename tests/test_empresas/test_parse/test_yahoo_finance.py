import time
import vcr
import pytest

from unittest import skip
from bfet import DjangoTestingModel as DTM

from apps.empresas.parse.others.yahoo_finance import ParseYahooFinance


parse_vcr = vcr.VCR(
    cassette_library_dir="cassettes/company/parse/yahoo_finance/",
    path_transformer=vcr.VCR.ensure_suffix(".yaml"),
)


@skip("Don't wnat to test")
from django.test import TestCase


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()
