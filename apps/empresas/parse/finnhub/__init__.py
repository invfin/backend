from apps.empresas.models import StatementsFinnhub
from apps.empresas.parse.finnhub.parse_data import ParseFinnhub


class FinnhubInfo(ParseFinnhub):
    def __init__(self, company) -> None:
        self.company = company

    def create_financials_finnhub(self):
        financials = self.financials_reported(symbol=self.company.ticker)
        StatementsFinnhub.objects.create(
            company=self.company,
            financials=financials,
        )
