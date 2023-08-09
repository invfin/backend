from typing import Union

from .utils import divide_or_zero, modify_for_percentage


class GrowthRates:
    @classmethod
    def calculate_growth_rate(
        cls,
        current_data: Union[int, float],
        previous_year_data: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero((current_data - previous_year_data), previous_year_data)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_revenue_growth(
        cls,
        current_revenue: Union[float, int],
        previous_revenue: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_revenue, previous_revenue)

    @classmethod
    def calculate_cost_revenue_growth(
        cls,
        current_cost_revenue: Union[float, int],
        previous_cost_revenue: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_cost_revenue, previous_cost_revenue)

    @classmethod
    def calculate_operating_expenses_growth(
        cls,
        current_operating_expenses: Union[float, int],
        previous_operating_expenses: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(
            current_operating_expenses, previous_operating_expenses
        )

    @classmethod
    def calculate_net_income_growth(
        cls,
        current_net_income: Union[float, int],
        previous_net_income: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_net_income, previous_net_income)

    @classmethod
    def calculate_shares_buyback(
        cls,
        current_shares_: Union[float, int],
        previous_shares_: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_shares_, previous_shares_)

    @classmethod
    def calculate_eps_growth(
        cls,
        current_eps: Union[float, int],
        previous_eps: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_eps, previous_eps)

    @classmethod
    def calculate_fcf_growth(
        cls,
        current_fcf: Union[float, int],
        previous_fcf: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_fcf, previous_fcf)

    @classmethod
    def calculate_owners_earnings_growth(
        cls,
        current_owners_earnings: Union[float, int],
        previous_owners_earnings: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_owners_earnings, previous_owners_earnings)

    @classmethod
    def calculate_capex_growth(
        cls,
        current_capex: Union[float, int],
        previous_capex: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_capex, previous_capex)

    @classmethod
    def calculate_rd_expenses_growth(
        cls,
        current_rd_expenses: Union[float, int],
        previous_rd_expenses: Union[float, int],
    ) -> Union[float, int]:
        return cls.calculate_growth_rate(current_rd_expenses, previous_rd_expenses)
