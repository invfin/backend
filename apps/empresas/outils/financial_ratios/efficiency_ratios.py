from typing import Union


from .utils import divide_or_zero


class EfficiencyRatios:
    @classmethod
    def calculate_days_inventory_outstanding(cls, average_inventory: Union[int, float], cost_of_revenue:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(average_inventory, (cost_of_revenue * 365), 4)

    @classmethod
    def calculate_days_payables_outstanding(cls, account_payables:Union[int, float], cost_of_goods_sold:Union[int, float],) -> Union[int, float]:
        return divide_or_zero((account_payables*365), cost_of_goods_sold, 3)

    @classmethod
    def calculate_days_sales_outstanding(cls, accounts_receivables:Union[int, float], account_payables:Union[int, float],) -> Union[int, float]:
        return divide_or_zero((accounts_receivables*365), account_payables, 3)

    @classmethod
    def calculate_operating_cycle(cls, days_inventory_outstanding:Union[int, float], days_sales_outstanding:Union[int, float],) -> Union[int, float]:
        return round(days_inventory_outstanding + days_sales_outstanding, 2)

    @classmethod
    def calculate_cash_conversion_cycle(cls, days_inventory_outstanding:Union[int, float], days_sales_outstanding:Union[int, float], days_payables_outstanding:Union[int, float],) -> Union[int, float]:
        return days_inventory_outstanding + days_sales_outstanding - days_payables_outstanding

    @classmethod
    def calculate_asset_turnover(cls, revenue:Union[int, float], average_assets:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(revenue, average_assets, 3)

    @classmethod
    def calculate_inventory_turnover(cls, cost_of_revenue:Union[int, float], average_inventory:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(cost_of_revenue, average_inventory, 3)

    @classmethod
    def calculate_fixed_asset_turnover(cls, revenue:Union[int, float], average_fixed_assets:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(revenue, average_fixed_assets, 3)

    @classmethod
    def calculate_payables_turnover(cls, accounts_payable:Union[int, float], cost_of_revenue:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(accounts_payable, cost_of_revenue, 3)

    @classmethod
    def calculate_fcf_to_operating_cf(cls, free_cash_flow:Union[int, float], net_cash_provided_by_operating_activities:Union[int, float],) -> Union[int, float]:
        return divide_or_zero(free_cash_flow, net_cash_provided_by_operating_activities, 3)
