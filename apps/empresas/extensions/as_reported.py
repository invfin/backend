from typing import List

from .base_averages import (
    AverageIncomeStatement,
    AverageBalanceSheet,
    AverageCashflowStatement,
)


class MapValuesFromDict:
    def get_financial_json_data_fields_to_map(self) -> List:
        return list(self.financial_data.keys())

    def get_own_field_to_map(self) -> List:
        base_class = self.__class__.__bases__[1]
        return list(base_class.__annotations__.keys())

    def save_mapped_fields(self, json_field: str, final_field: str):
        self.mapped_fields.update(
            {
                "json_field": json_field,
                "final_field": final_field,
            })

    def map_json_fields_with_regular(self):
        # TODO instead of running this each every time the mapping should be saved
        for field in self.get_own_field_to_map():
            field = field.replace("_field", "")
            value_found = self.financial_data.get(field)
            if value_found:
                self.save_mapped_fields(json_field, final_field)



class IncomeStatementAsReportedExtended(AverageIncomeStatement, MapValuesFromDict):
    pass

class BalanceSheetAsReportedExtended(AverageBalanceSheet, MapValuesFromDict):
    pass

class CashflowStatementAsReportedExtended(AverageCashflowStatement, MapValuesFromDict):
    pass
