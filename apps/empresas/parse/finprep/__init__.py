from typing import Type
from apps.empresas.models import BalanceSheetFinprep, IncomeStatementFinprep, CashflowStatementFinprep
from apps.empresas.parse.finprep.normalize_data import NormalizeFinprep
from apps.empresas.parse.finprep.parse_data import ParseFinprep


class FinprepInfo(NormalizeFinprep, ParseFinprep):
    def __init__(self, company: Type["Company"]) -> None:
        super().__init__(company)
        self.company: Type["Company"] = company

    def create_income_statements_finprep(self, list_income_statements_finprep=None):
        if not list_income_statements_finprep:
            list_income_statements_finprep = self.request_income_statements_finprep(self.company.ticker)
        for income_statements_finprep in list_income_statements_finprep:
            IncomeStatementFinprep.objects.create(
                **self.normalize_income_statements_finprep(income_statements_finprep)
            )

    def create_balance_sheets_finprep(self, list_balance_sheets_finprep=None):
        if not list_balance_sheets_finprep:
            list_balance_sheets_finprep = self.request_balance_sheets_finprep(self.company.ticker)
        for balance_sheets_finprep in list_balance_sheets_finprep:
            BalanceSheetFinprep.objects.create(
                **self.normalize_balance_sheets_finprep(balance_sheets_finprep)
            )

    def create_cashflow_statements_finprep(self, list_cashflow_statements_finprep=None):
        if not list_cashflow_statements_finprep:
            list_cashflow_statements_finprep = self.request_cashflow_statements_finprep(self.company.ticker)
        for cashflow_statements_finprep in list_cashflow_statements_finprep:
            CashflowStatementFinprep.objects.create(
                **self.normalize_cashflow_statements_finprep(cashflow_statements_finprep)
            )

    def create_financials_finprep(self):
        dict_financials_finprep = self.request_financials_finprep(self.company.ticker)
        dict_statements_actions = {
            "income_statements": self.create_income_statements_finprep,
            "balance_sheets": self.create_balance_sheets_finprep,
            "cashflow_statements": self.create_cashflow_statements_finprep,
        }
        for statement in ["income_statements", "balance_sheets", "cashflow_statements"]:
            dict_statements_actions[statement](dict_financials_finprep[statement])
