from typing import Union


from .utils import divide_or_zero


class EfficiencyRatios:
    @classmethod
    def calculate_days_inventory_outstanding(cls, average_inventory, cost_of_revenue) -> Union[int, float]:
        return divide_or_zero(average_inventory, cost_of_revenue)

    @classmethod
    def calculate_days_payables_outstanding(cls, accounts_payable, cost_of_goods_sold) -> Union[int, float]:
        return divide_or_zero((accounts_payable*360), cost_of_goods_sold)

    @classmethod
    def calculate_days_sales_outstanding(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_operating_cycle(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_cash_conversion_cycle(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_asset_turnover(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_inventory_turnover(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_fixed_asset_turnover(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_payables_turnover(cls,) -> Union[int, float]:
        return divide_or_zero()

    @classmethod
    def calculate_fcf_to_operating_cf(cls,) -> Union[int, float]:
        return divide_or_zero()
