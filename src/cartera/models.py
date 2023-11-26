from decimal import Decimal

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import (
    CASCADE,
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
from src.periods.models import Period
from src.users.models import User

from .constants import InvestmentMovement


class FirsttradeTransaction(AbstractTimeStampedModel):
    symbol = CharField(max_length=20, default="", blank=True)
    quantity = DecimalField(max_digits=100, decimal_places=3, null=True)
    price = DecimalField(max_digits=100, decimal_places=4, null=True)
    action = CharField(max_length=8)
    trade_date = DateField()
    settled_date = DateField()
    interest = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    amount = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    file_path = CharField(max_length=100)
    description = CharField(max_length=300, default="", blank=True)
    commission = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    fee = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    cusip = CharField(max_length=9, default="", blank=True)
    record_type = CharField(max_length=9)
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="firstrade_transactions",
    )

    class Meta:
        verbose_name = "Transaction from firstrade file"
        verbose_name_plural = "Transactions from firstrade file"
        db_table = "patrimoine_transactions_from_firstrade_file"

    def __str__(self) -> str:
        return f"{self.pk} firstrade"


class IngEsTransaction(AbstractTimeStampedModel):
    transaction_date = DateTimeField()
    category = CharField(max_length=300, default="", blank=True)
    subcaterogy = CharField(max_length=300, default="", blank=True)
    comment = CharField(max_length=300, default="", blank=True)
    image = CharField(max_length=300, default="", blank=True)
    amount = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    file_path = CharField(max_length=100)
    description = CharField(max_length=300, default="", blank=True)
    balance = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="ing_es_transactions",
    )
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "patrimoine_transactions_from_ing_es"

    def __str__(self) -> str:
        return f"{self.pk} IngEs"


class NetWorth(AbstractTimeStampedModel):
    user = ForeignKey(User, on_delete=SET_NULL, null=True, related_name="net_worth")
    amount = DecimalField(max_digits=100, decimal_places=3, default=Decimal(0.0))
    period = ForeignKey(Period, on_delete=SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "patrimoine_net_worth"

    def __str__(self) -> str:
        name = self.user or "Anon"
        return f"{self.pk} {name}"


class CashflowMovement(AbstractTimeStampedModel):
    name = CharField("Nombre", max_length=100)
    amount = DecimalField("Monto", max_digits=100, decimal_places=3, default=Decimal(0.0))
    description = TextField("Descripción", default="", blank=True)
    comment = TextField("Comentario", default="", blank=True)
    date = DateField("Fecha del movimiento", blank=True)
    currency = ForeignKey(Currency, on_delete=SET_NULL, null=True, blank=True)
    transaction_file_type = ForeignKey(ContentType, on_delete=SET_NULL, null=True)  # type: ignore TODO: add filters
    transaction_file_id = PositiveIntegerField(null=True)
    transaction_file = GenericForeignKey("transaction_file_type", "transaction_file_id")
    is_recurrent = BooleanField(default=False, blank=True)
    read = BooleanField(blank=True, default=False)
    amount_converted = DecimalField(
        max_digits=100,
        decimal_places=3,
        default=Decimal(0.0),
        blank=True,
    )

    class Meta:
        abstract = True
        ordering = ["-date"]

    def __str__(self) -> str:
        return self.name or "cashflow move"


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

    def __str__(self) -> str:
        return self.name or "Cashflow cat"


class Investment(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="investments",
    )
    content_type = ForeignKey(ContentType, on_delete=CASCADE, related_name="assets")  # type: ignore TODO: add filters
    object_id = PositiveIntegerField()
    object = GenericForeignKey("content_type", "object_id")
    quantity = DecimalField("Cantidad", max_digits=100, decimal_places=3, default=Decimal(0.0))
    price = DecimalField("Precio", max_digits=100, decimal_places=3, default=Decimal(0.0))
    movement = CharField("Moviemiento", max_length=4, choices=InvestmentMovement.to_choices())
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)
    net_worth = ForeignKey(
        NetWorth,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="net_worth_investments",
    )

    class Meta:
        verbose_name = "Investment"
        verbose_name_plural = "Investment"
        db_table = "patrimoine_investments"


class Income(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="incomes",
    )
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)
    content_type = ForeignKey(
        ContentType,
        on_delete=SET_NULL,
        null=True,
        related_name="assets_income",
    )  # type: ignore TODO: add filters
    object_id = PositiveIntegerField(blank=True, null=True)
    object = GenericForeignKey("content_type", "object_id")
    net_worth = ForeignKey(
        NetWorth,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="net_worth_incomes",
    )

    class Meta:
        db_table = "patrimoine_income"


class Spendings(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="spendings",
    )
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)
    net_worth = ForeignKey(
        NetWorth,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="net_worth_spendings",
    )

    class Meta:
        db_table = "patrimoine_spendings"


class Savings(CashflowMovement):
    user = ForeignKey(
        User,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="savings",
    )
    category = ForeignKey(CashflowMovementCategory, on_delete=SET_NULL, null=True, blank=True)
    net_worth = ForeignKey(
        NetWorth,
        on_delete=SET_NULL,
        null=True,
        blank=True,
        related_name="net_worth_savings",
    )

    class Meta:
        db_table = "patrimoine_savings"


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
        decimal_places=3,
        default=Decimal(0.0),
    )
    amount = DecimalField("Monto", max_digits=100, decimal_places=3, default=Decimal(0.0))
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
