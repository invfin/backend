from typing import Any

from bfet import DjangoTestingModel

from src.empresas.models import (
    Company,
)
from src.periods.constants import PERIOD_FOR_YEAR
from src.periods.models import Period


class NormalizeStatementMixin:
    company: Company
    period: Period
    income_statement: Any
    balance_sheet: Any
    cashflow_statement: Any
    income_statement_model: Any = None
    balance_sheet_model: Any = None
    cashflow_statement_model: Any = None

    @classmethod
    def setUpTestData(cls):
        cls.company = DjangoTestingModel.create(Company)  # type: ignore
        cls.period = DjangoTestingModel.create(Period, year=2021, period=PERIOD_FOR_YEAR)  # type: ignore
        cls.income_statement = DjangoTestingModel.create(
            cls.income_statement_model,
            company=cls.company,
            period=cls.period,
        )
        cls.balance_sheet = DjangoTestingModel.create(
            cls.balance_sheet_model,
            company=cls.company,
            period=cls.period,
        )
        cls.cashflow_statement = DjangoTestingModel.create(
            cls.cashflow_statement_model,
            company=cls.company,
            period=cls.period,
        )
