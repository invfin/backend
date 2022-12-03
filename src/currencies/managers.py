from typing import Type

from django.db.models import Manager


class CurrencyManager(Manager):
    def financial_currency(self, currency) -> Type:
        currency, created = self.get_or_create(currency=currency)
        return currency
