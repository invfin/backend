from statistics import mean
from typing import Type, List, Dict
from collections import Counter


class AverageStatements:
    def __init__(self, company) -> None:
        self.company = company

    def return_averaged_data(self, period: Type["Period"], statements: List[Type]):
        reunited_data = self.prepare_data(statements)
        currency = self.find_correct_currency(reunited_data)
        reunited_data = self.calculate_averages(reunited_data)
        reunited_data.update({"date": period.year, "period_id": period.id, **currency})
        print(reunited_data)
        return reunited_data

    def find_correct_currency(self, reunited_data: dict) -> Dict[str, int]:
        currency = reunited_data.pop("reported_currency_id", None)
        if currency:
            counter = Counter(currency)
            currency, repetitions = counter.most_common(1)[0]
        return {"reported_currency_id": currency}

    def calculate_averages(self, reunited_data: dict):
        for key in reunited_data.keys():
            reunited_data[key] = mean(reunited_data[key])
        return reunited_data

    def prepare_data(self, statements):
        reunited_data = {}
        for statement in statements:
            if statement:
                for key, value in statement.return_standard.items():
                    if value:
                        if key in reunited_data:
                            reunited_data[key].append(value)
                        else:
                            reunited_data[key] = [value]
        return reunited_data

    def calculate_average_income_statement(self, period):
        income_statement_finprep = self.company.incomestatementfinprep_set.filter(period=period).first()
        income_statement_yfinance = self.company.incomestatementyfinance_set.filter(period=period).first()
        income_statement_yahooquery = self.company.incomestatementyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [income_statement_finprep, income_statement_yfinance, income_statement_yahooquery]
        )

    def calculate_average_balance_sheet(self, period):
        balance_sheet_finprep = self.company.balancesheetfinprep_set.filter(period=period).first()
        balance_sheet_yfinance = self.company.balancesheetyfinance_set.filter(period=period).first()
        balance_sheet_yahooquery = self.company.balancesheetyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [balance_sheet_finprep, balance_sheet_yfinance, balance_sheet_yahooquery]
        )

    def calculate_average_cashflow_statement(self, period):
        cashflow_statement_finprep = self.company.cashflowstatementfinprep_set.filter(period=period).first()
        cashflow_statement_yfinance = self.company.cashflowstatementyfinance_set.filter(period=period).first()
        cashflow_statement_yahooquery = self.company.cashflowstatementyahooquery_set.filter(period=period).first()
        return self.return_averaged_data(
            period, [cashflow_statement_finprep, cashflow_statement_yfinance, cashflow_statement_yahooquery]
        )
