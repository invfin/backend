from collections import Counter
from statistics import mean
from typing import Any, Dict, List, Optional, Type


class AverageStatements:
    """
    Used to calculate the average over different financial sources

    Attributes
    ----------
        company
            The company to get the statements from. Set it when initializing the class.

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

    def find_correct_currency(self, reunited_data: dict) -> Dict[str, Any]:
        currency = reunited_data.pop("reported_currency_id", None)
        if currency:
            counter = Counter(currency)
            currency, repetitions = counter.most_common(1)[0]
        return {"reported_currency_id": currency}

    def calculate_averages(self, reunited_data: Dict) -> Dict[str, Any]:
        for key in reunited_data.keys():
            reunited_data[key] = mean(reunited_data[key])
        return reunited_data

    def prepare_data(self, statements: List) -> Optional[Dict[str, Any]]:
        reunited_data: Dict = {}
        for statement in statements:
            if statement:
                for key, value in statement.return_standard.items():
                    if value:
                        # value = abs(value)
                        if key in reunited_data:
                            reunited_data[key].append(value)
                        else:
                            reunited_data[key] = [value]
        return reunited_data

    def return_averaged_data(self, period, statements: List[Type]) -> Optional[Dict[str, Any]]:
        reunited_data = self.prepare_data(statements)
        if reunited_data:
            currency = self.find_correct_currency(reunited_data)
            reunited_data = self.calculate_averages(reunited_data)
            reunited_data.update({"date": period.year, "period_id": period.id, **currency})
            return reunited_data
        return None

    def calculate_average_income_statement(self, period) -> Optional[Dict[str, Any]]:
        return self.return_averaged_data(
            period,
            [
                self.company.incomestatementfinprep_set.filter(period=period).first(),
                self.company.incomestatementyfinance_set.filter(period=period).first(),
                self.company.incomestatementyahooquery_set.filter(period=period).first(),
            ],
        )

    def calculate_average_balance_sheet(self, period) -> Optional[Dict[str, Any]]:
        return self.return_averaged_data(
            period,
            [
                self.company.balancesheetfinprep_set.filter(period=period).first(),
                self.company.balancesheetyfinance_set.filter(period=period).first(),
                self.company.balancesheetyahooquery_set.filter(period=period).first(),
            ],
        )

    def calculate_average_cashflow_statement(self, period) -> Optional[Dict[str, Any]]:
        return self.return_averaged_data(
            period,
            [
                self.company.cashflowstatementfinprep_set.filter(period=period).first(),
                self.company.cashflowstatementyfinance_set.filter(period=period).first(),
                self.company.cashflowstatementyahooquery_set.filter(period=period).first(),
            ],
        )
