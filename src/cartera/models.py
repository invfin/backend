from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    SET_NULL,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    DecimalField,
    ForeignKey,
    JSONField,
    PositiveIntegerField,
    TextField,
)

from src.currencies.models import Currency
from src.general.abstracts import AbstractTimeStampedModel
from src.users.models import User


class CashflowMovement(AbstractTimeStampedModel):
    name = CharField("Nombre", max_length=100)
    amount = DecimalField("Monto", max_digits=100, decimal_places=2, default=Decimal(0.0))
    description = TextField("Descripción", default="")
    date = DateField("Fecha del movimiento", null=True, blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True
        ordering = ["-date"]

    def __str__(self):
        return self.name


class InvestmentMovement(CashflowMovement):
    content_type = ForeignKey(ContentType, on_delete=SET_NULL, null=True)  # type: ignore
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    quantity = PositiveIntegerField("Cantidad")
    price = DecimalField("Precio", max_digits=100, decimal_places=2, default=Decimal(0.0))

    class Meta:
        abstract = True


class BuyInvestment(InvestmentMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="investments_buy",
    )

    class Meta:
        verbose_name = "Investment buys"
        verbose_name_plural = "Investment buys"
        db_table = "patrimoine_investments_buy"


class SellInvestment(InvestmentMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="investments_sell",
    )

    class Meta:
        verbose_name = "Investemnt sell"
        verbose_name_plural = "Investement sells"
        db_table = "patrimoine_investments_sells"


class CashflowMovementCategory(AbstractTimeStampedModel):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="cashflow_movement_categories",
    )
    name = CharField("Nombre", max_length=100)

    class Meta:
        verbose_name = "Cashflow category"
        verbose_name_plural = "Cashflow categories"
        db_table = "patrimoine_cashflow_category"

    def __str__(self):
        return self.name


class Income(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="incomes",
    )
    is_recurrent = BooleanField(default=False)
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "patrimoine_income"


class Spend(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="spends",
    )
    is_recurrent = BooleanField(default=False)
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "patrimoine_spend"


class Saving(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="savings",
    )
    is_recurrent = BooleanField(default=False)
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "patrimoine_saving"


class FinancialObjectif(AbstractTimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, blank=True)
    name = CharField("Nombre", max_length=100)
    date_created = DateTimeField(auto_now_add=True)
    date_to_achieve = DateTimeField(null=True, blank=True)
    date_achived = DateTimeField(null=True, blank=True)
    observation = TextField("Observaciones", default="")
    accomplished = BooleanField(default=False)
    abandoned = BooleanField(default=False)
    percentage = DecimalField(
        "Porcentaje",
        max_digits=100,
        decimal_places=2,
        default=Decimal(0.0),
    )
    amount = DecimalField("Monto", max_digits=100, decimal_places=2, default=Decimal(0.0))
    is_rule = BooleanField(default=False)
    rule_ends = BooleanField(default=False)
    requirement = JSONField(default=dict)
    start_date = DateTimeField(null=True, blank=True)
    end_date = DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["date_created"]
        verbose_name = "Objetivo financiero"
        verbose_name_plural = "Objetivo financieros"
        db_table = "patrimoine_objectives"

    def __str__(self):
        return self.name
