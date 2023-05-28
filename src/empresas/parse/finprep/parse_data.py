import random
import time
from typing import Dict, List, Optional, Union

from django.conf import settings

from src.empresas import constants
from src.general.outils.parser_client import ParserClient


class ParseFinprep(ParserClient):
    base_path = constants.FINPREP_BASE_URL
    api_version = "v3"
    auth = {"apikey": settings.FINPREP_KEY}

    def request_income_statements_finprep(
        self,
        ticker,
        dict_params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> List:
        dict_params = dict_params or {"limit": 120}
        return self.request(
            path="income-statement", str_params=ticker, dict_params=dict_params
        )

    def request_balance_sheets_finprep(
        self,
        ticker,
        dict_params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> List:
        dict_params = dict_params or {"limit": 120}
        return self.request(
            path="balance-sheet-statement", str_params=ticker, dict_params=dict_params
        )

    def request_cashflow_statements_finprep(
        self,
        ticker,
        dict_params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> List:
        dict_params = dict_params or {"limit": 120}
        return self.request(
            path="cash-flow-statement", str_params=ticker, dict_params=dict_params
        )

    def request_financials_finprep(
        self,
        ticker,
        dict_params: Optional[Dict[str, Union[str, int]]] = None,
    ) -> Dict[str, List]:
        dict_params = dict_params or {"limit": 120}
        income_statements = self.request_income_statements_finprep(ticker, dict_params)
        time.sleep(random.randint(5, 10))
        balance_sheets = self.request_balance_sheets_finprep(ticker, dict_params)
        time.sleep(random.randint(5, 10))
        cashflow_statements = self.request_cashflow_statements_finprep(ticker, dict_params)
        return {
            "income_statements": income_statements,
            "balance_sheets": balance_sheets,
            "cashflow_statements": cashflow_statements,
        }
