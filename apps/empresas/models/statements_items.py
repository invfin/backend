from django.db.models import (
    SET_NULL,
    ForeignKey,
    DecimalField,
    CharField,
    PROTECT,
)

from apps.general.abstracts import AbstractTimeStampedModel


class StatementItemConcept(AbstractTimeStampedModel):
    concept = CharField(max_length=350)
    unit = CharField(max_length=50)
    label = CharField(max_length=350)
    company = ForeignKey(
        "empresas.Company",
        on_delete=SET_NULL,
        null=True,
        related_name="unique_statements_items",
    )

    class Meta:
        db_table = "assets_statements_items_concepts"

    @property
    def is_unique_for_company(self) -> bool:
        return bool(self.company)


class StatementItem(AbstractTimeStampedModel):
    concept = ForeignKey(StatementItemConcept, on_delete=PROTECT)
    value = DecimalField()
    currency = ForeignKey("currencies.Currency", on_delete=SET_NULL, null=True)

    class Meta:
        db_table = "assets_statements_items"
