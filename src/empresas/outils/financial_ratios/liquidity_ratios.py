from typing import Union

from .utils import divide_or_zero


class LiquidityRatios:
    @classmethod
    def calculate_cash_ratio(
        cls,
        cash_and_cash_equivalents: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(cash_and_cash_equivalents, total_current_liabilities)

    @classmethod
    def calculate_current_ratio(
        cls,
        total_current_assets: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_current_assets, total_current_liabilities)

    @classmethod
    def calculate_quick_ratio(
        cls,
        net_receivables: Union[int, float],
        cash_and_short_term_investments: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero((net_receivables + cash_and_short_term_investments), total_current_liabilities)

    @classmethod
    def calculate_operating_cashflow_ratio(
        cls,
        net_cash_provided_by_operating_activities: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(net_cash_provided_by_operating_activities, total_current_liabilities)

    @classmethod
    def calculate_debt_to_equity(
        cls,
        total_liabilities: Union[int, float],
        total_stockholders_equity: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_liabilities, total_stockholders_equity)
