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
            field_filtered = self.fields.filter(concept__concept_slug=field_name)
            print(field_name)
            print(field_filtered)
            if field_filtered.exists():
                if field_filtered.filter(concept__corresponding_final_item__isnull=True).exists():
                    field_filtered.update(concept__corresponding_final_item=field)
            else:
                self.match_field(field, field_name)

    def match_field(self, field: str, field_name: str):
        label_slug_filtered = self.fields.filter(concept__label_slug=field_name)
        print(label_slug_filtered)
        if label_slug_filtered.exists():
            if label_slug_filtered.filter(concept__corresponding_final_item__isnull=True).exists():
                label_slug_filtered.update(concept__corresponding_final_item=field)

    def mapped_fields(self):
        return self.fields.filter(concept__corresponding_final_item__isnull=False)


class IncomeStatementAsReportedExtended(AverageIncomeStatement, MapValuesFromDict):
    pass


class BalanceSheetAsReportedExtended(AverageBalanceSheet, MapValuesFromDict):
    pass


class CashflowStatementAsReportedExtended(AverageCashflowStatement, MapValuesFromDict):
    pass
