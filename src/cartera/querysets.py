from src.general.managers import BaseQuerySet
from decimal import Decimal
from django.db.models import Sum


class CashflowMovementQuerySet(BaseQuerySet):
    def get_total(self) -> "CashflowMovementQuerySet":
        result = self.aggregate(Sum("amount_converted")).get("amount_converted__sum")
        return result or Decimal(0.0)
