from statistics import mean
from typing import Type, List, Dict, Union, Any
from collections import Counter


class AverageStatements:
    """
    Used to calculate the average over different financial sources

    Attributes
    ----------
        company: Type["Company"]
            The company to get the statements from. Set it when initializing the class.

    Methods
    -------
        return_averaged_data:
            Method that accepts a list of statements and a specific period. It then to the calculations, find the currency
            and returns a dict with the information for the new statement.

        find_correct_currency:
            Method that get a list of currencies IDs and find the most common.

        calculate_averages:
            Method that get a list of values and calculates the mean.

        prepare_data:
            Method that loops over the statements and builds a dict with the fields for the multiples statements, the values of
            all the statements related to the company and the period.

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

    def __init__(self, company: Type["Company"]) -> None:
        self.company = company

    def return_averaged_data(self, period: Type["Period"], statements: List[Type]) -> Union[Dict[str, Any], None]:
        reunited_data = self.prepare_data(statements)
        if reunited_data:
            currency = self.find_correct_currency(reunited_data)
            reunited_data = self.calculate_averages(reunited_data)
            reunited_data.update({"date": period.year, "period_id": period.id, **currency})
            return reunited_data
        return None

    def find_correct_currency(self, reunited_data: dict) -> Dict[str, int]:
        currency = reunited_data.pop("reported_currency_id", None)
        if currency:
            counter = Counter(currency)
            currency, repetitions = counter.most_common(1)[0]
        return {"reported_currency_id": currency}

    def calculate_averages(self, reunited_data: dict) -> Dict[str, Any]:
        for key in reunited_data.keys():
            reunited_data[key] = mean(reunited_data[key])
        return reunited_data

    def prepare_data(self, statements: list) -> Union[Dict[str, Any], None]:
        reunited_data = {}
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

    def calculate_average_income_statement(self, period: Type["Period"]) -> Union[Dict[str, Any], None]:
        income_statement_finprep = self.company.incomestatementfinprep_set.filter(period=period).first()
        income_statement_yfinance = self.company.incomestatementyfinance_set.filter(period=period).first()
        income_statement_yahooquery = self.company.incomestatementyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [income_statement_finprep, income_statement_yfinance, income_statement_yahooquery]
        )

    def calculate_average_balance_sheet(self, period: Type["Period"]) -> Union[Dict[str, Any], None]:
        balance_sheet_finprep = self.company.balancesheetfinprep_set.filter(period=period).first()
        balance_sheet_yfinance = self.company.balancesheetyfinance_set.filter(period=period).first()
        balance_sheet_yahooquery = self.company.balancesheetyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [balance_sheet_finprep, balance_sheet_yfinance, balance_sheet_yahooquery]
        )

    def calculate_average_cashflow_statement(self, period: Type["Period"]) -> Union[Dict[str, Any], None]:
        cashflow_statement_finprep = self.company.cashflowstatementfinprep_set.filter(period=period).first()
        cashflow_statement_yfinance = self.company.cashflowstatementyfinance_set.filter(period=period).first()
        cashflow_statement_yahooquery = self.company.cashflowstatementyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [cashflow_statement_finprep, cashflow_statement_yfinance, cashflow_statement_yahooquery]
        )
