from typing import List, Dict, Union, Any
import requests
import time
import random

from django.conf import settings

from apps.general.outils.parser_client import ParserClient
from apps.empresas import constants
from apps.empresas.parse.finprep.normalize_data import NormalizeFinprep


class ParseFinprep:
    def base_request(
        self,
        path,
        api_version: str,
        str_params: str,
        dict_params: Dict[str, str] = {}
    ) -> Union[Dict[str, Any], str, requests.Response]:
        dict_params.update({"apikey": settings.FINPREP_KEY})
        return ParserClient().request(
            constants.FINPREP_BASE_URL,
            path=path,
            api_version=api_version,
            str_params=str_params,
            dict_params=dict_params
        )

    def request_income_statements_finprep(
        self,
        ticker,
        path: str = "income-statement",
        api_version: str = "v3",
        dict_params: Dict[str, str] = {"limit": 120}
    ) -> list:
        return self.base_request(
            path=path,
            api_version=api_version,
            str_params=ticker,
            dict_params=dict_params
        )

    def request_balance_sheets_finprep(self,
        ticker,
        path: str = "balance-sheet-statement",
        api_version: str = "v3",
        dict_params: Dict[str, str] = {"limit": 120}
    ) -> list:
        return self.base_request(
            path=path,
            api_version=api_version,
            str_params=ticker,
            dict_params=dict_params
        )

    def request_cashflow_statements_finprep(self,
        ticker,
        path: str = "cash-flow-statement",
        api_version: str = "v3",
        dict_params: Dict[str, str] = {"limit": 120}
    ) -> list:
        return self.base_request(
            path=path,
            api_version=api_version,
            str_params=ticker,
            dict_params=dict_params
        )

    def request_finprep_financials(
        self,
        ticker,
        api_version: str = "v3",
        dict_params: Dict[str, str] = {"limit": 120}
    ) -> Dict[str, List]:
        random_int = random.randint(5, 10)
        income_statements = self.request_income_statements_finprep(
            ticker,
            api_version=api_version,
            dict_params=dict_params
        )
        time.sleep(random_int)
        balance_sheets = self.request_balance_sheets_finprep(
            ticker,
            api_version=api_version,
            dict_params=dict_params
        )
        time.sleep(random_int)
        cashflow_statements = self.request_cashflow_statements_finprep(
            ticker,
            api_version=api_version,
            dict_params=dict_params
        )
        return {
            "income_statements": income_statements,
            "balance_sheets": balance_sheets,
            "cashflow_statements": cashflow_statements,
        }
