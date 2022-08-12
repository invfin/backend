import vcr

from django.test import TestCase

from apps.empresas.parse.finprep import ParseFinprep
from apps.empresas.tests import finprep_data


parse_vcr = vcr.VCR(
    cassette_library_dir='cassettes/company/parse/finprep/',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
)


class TestParseFinprep(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.parser = ParseFinprep()

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_income_statements_finprep(self):
        comp_data = self.parser.request_income_statements_finprep("AAPL")
        self.assertEqual(finprep_data.INCOME_STATEMENT, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_balance_sheets_finprep(self):
        comp_data = self.parser.request_balance_sheets_finprep("AAPL")
        self.assertEqual(finprep_data.BALANCE_SHEET, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_cashflow_statements_finprep(self):
        comp_data = self.parser.request_cashflow_statements_finprep("AAPL")
        self.assertEqual(finprep_data.CASHFLOW_STATEMENT, comp_data)

    @parse_vcr.use_cassette(filter_query_parameters=['apikey'])
    def test_request_finprep_financials(self):
        comp_data = self.parser.request_finprep_financials("AAPL")
        self.assertEqual(finprep_data.DICT_STATEMENTS, comp_data)
