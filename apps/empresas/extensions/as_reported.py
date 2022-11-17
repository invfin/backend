from typing import List

from django.db.models import F
from django.template.defaultfilters import slugify

from .base_averages import (
    AverageIncomeStatement,
    AverageBalanceSheet,
    AverageCashflowStatement,
)


class MapValuesFromDict:
    def get_own_field_to_map(self) -> List:
        base_class = self.__class__.__bases__[1]
        return list(base_class.__annotations__.keys())

    def map_fields(self):
        for field in self.get_own_field_to_map():
            field_name = field.replace("_field", "")
            field_filtered = self.fields.filter(slug=field_name)
            if field_filtered.exists():
                if field_filtered.filter(corresponding_final_item__isnull=True).exists():
                    field_filtered.update(corresponding_final_item=field)
            else:
                self.match_field(field, field_name)

    def match_field(self, field: str, field_name: str):
        slug_label_filtered = self.fields.all().annotate(slug_label=slugify(F("label"))).filter(slug_label=field_name)
        if slug_label_filtered.exists():
            slug_label_filtered.update(corresponding_final_item=field)

    def mapped_fields(self):
        return self.fields.filter(corresponding_final_item__isnull=False)


class IncomeStatementAsReportedExtended(AverageIncomeStatement, MapValuesFromDict):
    pass


class BalanceSheetAsReportedExtended(AverageBalanceSheet, MapValuesFromDict):
    pass


class CashflowStatementAsReportedExtended(AverageCashflowStatement, MapValuesFromDict):
    pass
