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
        base_class, extended_class = self.__class__.__bases__
        if extended_class.__name__.endswith("AsReportedExtended"):
            return list(extended_class().__annotations__.keys())
        else:
            raise Exception("The class doesn't match with AsReportedExtended")


    def map_fields(self):
        for field in self.get_own_field_to_map():
            field_name = field.replace("_field", "")
            field_filtered = self.fields.filter(concept__concept_slug=field_name)
            if field_filtered.exists():
                if field_filtered.filter(concept__corresponding_final_item="").exists():
                    for item_field in field_filtered:
                        item_field.concept.corresponding_final_item=field
                        item_field.concept.save(update_fields=["corresponding_final_item"])
            else:
                self.match_field(field, field_name)

    def match_field(self, field: str, field_name: str):
        label_slug_filtered = self.fields.filter(concept__label_slug=field_name)
        if label_slug_filtered.exists():
            if label_slug_filtered.filter(concept__corresponding_final_item="").exists():
                for item_field in label_slug_filtered:
                    item_field.concept.corresponding_final_item = field
                    item_field.concept.save(update_fields=["corresponding_final_item"])

    def mapped_fields(self):
        return self.fields.filter(concept__corresponding_final_item="")


class IncomeStatementAsReportedExtended(AverageIncomeStatement, MapValuesFromDict):
    pass


class BalanceSheetAsReportedExtended(AverageBalanceSheet, MapValuesFromDict):
    pass


class CashflowStatementAsReportedExtended(AverageCashflowStatement, MapValuesFromDict):
    pass
