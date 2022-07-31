from model_bakery import baker

from apps.users.tests.factories import regular_user

from apps.cartera.models import (
Asset,
CashflowMovement,
CashflowMovementCategory,
FinancialObjectif,
Income,
Patrimonio,
PositionMovement,
Spend,
)


baker.make(Asset)
baker.make(CashflowMovement)
baker.make(CashflowMovementCategory)
baker.make(FinancialObjectif)
baker.make(Income)
baker.make(Patrimonio)
baker.make(PositionMovement)
baker.make(Spend)