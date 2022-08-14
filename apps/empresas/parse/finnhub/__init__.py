from apps.empresas.models import StatementsFinnhub
from apps.empresas.parse.finnhub.parse_data import ParseFinnhub


class FinnhubInfo(ParseFinnhub):
    def __init__(self, company) -> None:
        super().__init__()
        self.company = company

    def save_financials_as_reported(self):
        financials = self.financials_reported(symbol=self.company.ticker)
        StatementsFinnhub.objects.create(
            company=self.company,
            financials=financials,
        )
