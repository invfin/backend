from typing import Union


from .utils import divide_or_zero


class PerShareValues:
    round_after_coma: int = 4

    @classmethod
    def calculate_sales_ps(
        cls,
        revenue: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        print(revenue, weighted_average_shares_out)
        return divide_or_zero(revenue, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_book_ps(
        cls,
        total_stockholders_equity: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_stockholders_equity, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_tangible_ps(
        cls,
        net_tangible_equity: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(net_tangible_equity, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_fcf_ps(
        cls,
        free_cash_flow: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(free_cash_flow, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_eps(
        cls,
        net_income: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(net_income, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_cash_ps(
        cls,
        cash_and_short_term_investments: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(cash_and_short_term_investments, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_operating_cf_ps(
        cls,
        net_cash_provided_by_operating_activities: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(
            net_cash_provided_by_operating_activities, weighted_average_shares_out, cls.round_after_coma
        )

    @classmethod
    def calculate_capex_ps(
        cls,
        capital_expenditure: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(capital_expenditure, weighted_average_shares_out, cls.round_after_coma)

    @classmethod
    def calculate_total_assets_ps(
        cls,
        total_assets: Union[int, float],
        weighted_average_shares_out: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_assets, weighted_average_shares_out, cls.round_after_coma)
