from ...models.finprep import BalanceSheetFinprep
from apps.empresas.parse.finprep.normalize_data import NormalizeFinprep
from apps.empresas.parse.finprep.parse_data import ParseFinprep


class FinprepInfo(NormalizeFinprep, ParseFinprep):
    def build_statements_finprep(self):
        self.request_finprep_financials()
