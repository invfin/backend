from typing import Union


from .utils import divide_or_zero, modify_for_percentage


class OtherRatios:
    @classmethod
    def calculate_average_fixed_assets(
        cls,
        last_year_fixed_assets: Union[int, float],
        property_plant_equipment_net: Union[int, float],
    ) -> Union[int, float]:
        return round((last_year_fixed_assets + property_plant_equipment_net) / 2, 2)

    @classmethod
    def calculate_average_assets(
        cls,
        last_year_assets: Union[int, float],
        total_assets: Union[int, float],
    ) -> Union[int, float]:
        return round((last_year_assets + total_assets) / 2, 2)

    @classmethod
    def calculate_net_working_capital(
        cls,
        total_current_assets: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return total_current_assets - total_current_liabilities

    @classmethod
    def calculate_change_in_working_capital(
        cls,
        net_working_capital: Union[int, float],
        last_year_current_assets: Union[int, float],
        last_year_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return net_working_capital - last_year_current_assets - last_year_current_liabilities

    @classmethod
    def calculate_gross_invested_capital(
        cls,
        net_working_capital: Union[int, float],
        property_plant_equipment_net: Union[int, float],
        depreciation_and_amortization: Union[int, float],
    ) -> Union[int, float]:
        return net_working_capital + property_plant_equipment_net + depreciation_and_amortization

    @classmethod
    def calculate_effective_tax_rate(
        cls,
        income_tax_expense: Union[int, float],
        operating_income: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(income_tax_expense, operating_income)

    @classmethod
    def calculate_net_tangible_equity(
        cls,
        total_current_assets: Union[int, float],
        property_plant_equipment_net: Union[int, float],
        total_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return total_current_assets + property_plant_equipment_net - total_liabilities

    @classmethod
    def calculate_nopat(
        cls,
        operating_income: Union[int, float],
        income_tax_expense: Union[int, float],
    ) -> Union[int, float]:
        first_result = divide_or_zero(income_tax_expense, operating_income)
        return operating_income * (1 - first_result)

    @classmethod
    def calculate_debt_and_equity(
        cls,
        total_debt: Union[int, float],
        total_stockholders_equity: Union[int, float],
    ) -> Union[int, float]:
        return total_debt + total_stockholders_equity

    @classmethod
    def calculate_non_cash_working_capital(
        cls,
        non_cash_working_capital: Union[int, float],
        cash_and_cash_equivalents: Union[int, float],
    ) -> Union[int, float]:
        return non_cash_working_capital - cash_and_cash_equivalents

    @classmethod
    def calculate_invested_capital(
        cls,
        property_plant_equipment_net: Union[int, float],
        non_cash_working_capital: Union[int, float],
    ) -> Union[int, float]:
        return property_plant_equipment_net + non_cash_working_capital
