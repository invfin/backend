from typing import Union


from .utils import divide_or_zero


class EfficiencyRatios:
    @classmethod
    def calculate_days_inventory_outstanding(
        cls,
        average_inventory: Union[int, float],
        cost_of_goods_sold: Union[int, float],
        period_measured: Union[int, float] = 365,
    ) -> Union[int, float]:
        return divide_or_zero(average_inventory, (cost_of_goods_sold * period_measured), 4)

    @classmethod
    def calculate_days_payable_outstanding(
        cls,
        accounts_payable: Union[int, float],
        cost_of_goods_sold: Union[int, float],
        period_measured: Union[int, float] = 365,
    ) -> Union[int, float]:
        return divide_or_zero((accounts_payable * period_measured), cost_of_goods_sold, 3)

    @classmethod
    def calculate_net_credit_sales(
        cls,
        sales_on_credit: Union[int, float],
        sales_returns: Union[int, float],
        sales_allowances: Union[int, float],
    ) -> Union[int, float]:
        return sales_on_credit - sales_returns - sales_allowances

    @classmethod
    def calculate_days_sales_outstanding(
        cls,
        accounts_receivable: Union[int, float],
        net_credit_sales: Union[int, float],
        period_measured: Union[int, float] = 365,
    ) -> Union[int, float]:
        result = divide_or_zero(accounts_receivable, net_credit_sales, 3)
        return result * period_measured

    @classmethod
    def calculate_cash_conversion_cycle(
        cls,
        days_inventory_outstanding: Union[int, float],
        days_sales_outstanding: Union[int, float],
        days_payable_outstanding: Union[int, float],
    ) -> Union[int, float]:
        return days_inventory_outstanding + days_sales_outstanding - days_payable_outstanding


    @classmethod
    def calculate_asset_turnover(
        cls,
        revenue: Union[int, float],
        average_assets: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(revenue, average_assets, 3)

    @classmethod
    def calculate_inventory_turnover(
        cls,
        cost_of_revenue: Union[int, float],
        average_inventory: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(cost_of_revenue, average_inventory, 3)

    @classmethod
    def calculate_inventory_period(
        cls,
        inventory_turnover: Union[int, float],
        period: Union[int, float] = 365,
    ) -> Union[int, float]:
        return divide_or_zero(period, inventory_turnover, 3)

    @classmethod
    def calculate_average_accounts_receivable(
        cls,
        last_year_accounts_receivable: Union[int, float],
        accounts_receivable: Union[int, float],
    ) -> Union[int, float]:
        return (last_year_accounts_receivable + accounts_receivable) / 2

    @classmethod
    def calculate_receivables_turnover(
        cls,
        credit_sales: Union[int, float],
        average_accounts_receivable: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(credit_sales, average_accounts_receivable, 3)

    @classmethod
    def calculate_receivables_period(
        cls,
        receivables_turnover: Union[int, float],
        period: Union[int, float] = 365,
    ) -> Union[int, float]:
        return divide_or_zero(period, receivables_turnover, 3)

    @classmethod
    def calculate_operating_cycle(
        cls,
        inventory_period: Union[int, float],
        receivables_period: Union[int, float],
    ) -> Union[int, float]:
        return round(inventory_period + receivables_period, 2)

    @classmethod
    def calculate_fixed_asset_turnover(
        cls,
        net_sales: Union[int, float],
        average_fixed_assets: Union[int, float],
    ) -> Union[int, float]:
        # Net Sales=Gross sales, less returns, and allowances
        # commonly used as a metric in manufacturing industries that make
        # substantial purchases of PP&E in order to increase output
        return divide_or_zero(net_sales, average_fixed_assets, 3)

    @classmethod
    def calculate_average_accounts_payable(
        cls,
        last_year_accounts_payable: Union[int, float],
        accounts_payable: Union[int, float],
    ) -> Union[int, float]:
        return (last_year_accounts_payable + accounts_payable) / 2

    @classmethod
    def calculate_accounts_payable_turnover(
        cls,
        net_credit_purchase: Union[int, float],
        average_accounts_payable: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(net_credit_purchase, average_accounts_payable, 3)

    @classmethod
    def calculate_free_cashflow_to_operating_cashflow(
        cls,
        free_cash_flow: Union[int, float],
        net_cash_provided_by_operating_activities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(free_cash_flow, net_cash_provided_by_operating_activities, 3)
