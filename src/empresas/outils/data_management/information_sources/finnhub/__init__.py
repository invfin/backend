from src.empresas.models import StatementsFinnhub
from .parse_data import ParseFinnhub


class FinnhubInfo(ParseFinnhub):
    def __init__(self, company) -> None:
        self.company = company

    def create_financials_finnhub(self):
        financials = self.financials_reported(symbol=self.company.ticker)
        StatementsFinnhub.objects.get_or_create(
            company=self.company,
            financials=financials,
        )
