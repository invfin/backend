import time
import vcr

from django.test import TestCase

from apps.bfet import ExampleModel
from apps.empresas.parse.yahoo_query import ParseFinprep
from apps.empresas.tests import finprep_data


parse_vcr = vcr.VCR(
    cassette_library_dir='cassettes/company/parse/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()
