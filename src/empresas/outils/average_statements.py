from collections import Counter, defaultdict
from statistics import fmean
from typing import Any, Dict, List, Optional, Type, Union

from src.periods.models import Period


class AverageStatements:
    """
    Used to calculate the average over different financial sources

    Attributes
    ----------
        company
            The company to get the statements from.

    Methods
    -------
        return_averaged_data:
            Method that accepts a list of statements and a specific period.
            It then to the calculations, find the currency and returns a dict with the
            information for the new statement.

        find_correct_currency:
            Method that get a list of currencies IDs and find the most common.

        calculate_averages:
            Method that get a list of values and calculates the mean.

        prepare_data:
            Method that loops over the statements and builds a dict with the fields for
            the multiples statements, the values of all the statements related to the company and the period.

        calculate_average_income_statement:
            Method that filter according to the company and the period and get the first of all the statements.
            It returns the result of return_averaged_data

        calculate_average_balance_sheet:
            Method that filter according to the company and the period and get the first of all the statements.
            It returns the result of return_averaged_data

        calculate_average_cashflow_statement:
            Method that filter according to the company and the period and get the first of all the statements.
            It returns the result of return_averaged_data
    """

    def __init__(self, company) -> None:
        self.company = company

    def calculate_average_income_statement(
        self,
        period: Period,
    ) -> Optional[Dict[str, Union[int, float]]]:
        return self.return_averaged_data(
            period,
            [
                self.company.incomestatementfinprep_set.filter(period=period).first(),
                self.company.incomestatementyfinance_set.filter(period=period).first(),
                self.company.incomestatementyahooquery_set.filter(period=period).first(),
            ],
        )

    def calculate_average_balance_sheet(
        self,
        period: Period,
    ) -> Optional[Dict[str, Union[int, float]]]:
        return self.return_averaged_data(
            period,
            [
                self.company.balancesheetfinprep_set.filter(period=period).first(),
                self.company.balancesheetyfinance_set.filter(period=period).first(),
                self.company.balancesheetyahooquery_set.filter(period=period).first(),
            ],
        )

    def calculate_average_cashflow_statement(
        self,
        period: Period,
    ) -> Optional[Dict[str, Union[int, float]]]:
        return self.return_averaged_data(
            period,
            [
                self.company.cashflowstatementfinprep_set.filter(period=period).first(),
                self.company.cashflowstatementyfinance_set.filter(period=period).first(),
                self.company.cashflowstatementyahooquery_set.filter(period=period).first(),
            ],
        )

    @classmethod
    def return_averaged_data(
        cls,
        period: Period,
        statements: List[Type],
    ) -> Optional[Dict[str, Union[int, float]]]:
        if reunited_data := cls.prepare_data(statements):
            currency = cls.find_correct_currency(reunited_data)
            final_data = cls.calculate_averages(reunited_data)
            # TODO: check it it works
            final_data.update(**{"date": period.year, "period_id": period.id, **currency})
            return final_data
        return None

    @staticmethod
    def prepare_data(statements: List) -> Dict[str, List[Union[int, float]]]:
        reunited_data = defaultdict(list)
        for statement in statements:
            if statement:
                for key, value in statement.return_standard().items():
                    if value:
                        reunited_data[key].append(value)
        return reunited_data

    @staticmethod
    def find_correct_currency(
        reunited_data: Union[Dict[str, List[Union[int, float]]], defaultdict]
    ) -> Dict[str, Optional[int]]:
        if currency := reunited_data.pop("reported_currency_id", None):
            currency, repetitions = Counter(currency).most_common(1)[0]  # type: ignore
        return {"reported_currency_id": currency}  # type: ignore

    @staticmethod
    def calculate_averages(
        reunited_data: Dict[str, List[Union[int, float]]]
    ) -> Dict[str, Union[int, float]]:
        return {key: round(fmean(value), 2) for key, value in reunited_data.items()}
