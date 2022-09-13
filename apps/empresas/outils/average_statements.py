from statistics import mean


class AverageStatements:
    company = None

    def calculate_income_statement(self, period):
        self.company.incomestatementfinprep_set.get(period=period).return_standard
        self.company.incomestatementyfinance_set.get(period=period).return_standard
        self.company.incomestatementyahooQuery_set.get(period=period).return_standard

    def calculate_balance_sheet(self, period):
        self.company.balancesheetfinprep_set.get(period=period).return_standard
        self.company.balancesheetyfinance_set.get(period=period).return_standard
        self.company.balancesheetyahooQuery_set.get(period=period).return_standard

    def calculate_cashflow_statement(self, period):
        self.company.cashflowstatementfinprep_set.get(period=period).return_standard
        self.company.cashflowstatementyfinance_set.get(period=period).return_standard
        self.company.cashflowstatementyahooQuery_set.get(period=period).return_standard
