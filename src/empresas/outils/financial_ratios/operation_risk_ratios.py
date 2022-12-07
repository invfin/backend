from typing import Union


from .utils import divide_or_zero


class OperationRiskRatios:
    @classmethod
    def calcualte_asset_coverage_ratio(
        cls,
        total_assets: Union[int, float],
        goodwill_and_intangible_assets: Union[int, float],
        total_current_liabilities: Union[int, float],
        short_term_debt: Union[int, float],
        interest_expense: Union[int, float],
    ) -> Union[int, float]:
        total_assets_less_cash = (
            total_assets - goodwill_and_intangible_assets - total_current_liabilities - short_term_debt
        )
        return divide_or_zero(total_assets_less_cash, interest_expense)

    @classmethod
    def calcualte_cash_flow_coverage_ratios(
        cls, net_cash_provided_by_operating_activities: Union[int, float], total_debt: Union[int, float]
    ) -> Union[int, float]:
        return divide_or_zero(net_cash_provided_by_operating_activities, total_debt)

    @classmethod
    def calcualte_cash_coverage(
        cls,
        cash_and_short_term_investments: Union[int, float],
        interest_expense: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(cash_and_short_term_investments, interest_expense)

    @classmethod
    def calcualte_debt_service_coverage(
        cls,
        operating_income: Union[int, float],
        total_debt: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(operating_income, total_debt)

    @classmethod
    def calcualte_interest_coverage(
        cls,
        operating_income: Union[int, float],
        interest_expense: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(operating_income, interest_expense)

    @classmethod
    def calcualte_operating_cashflow_ratio(
        cls,
        net_cash_provided_by_operating_activities: Union[int, float],
        total_current_liabilities: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(net_cash_provided_by_operating_activities, total_current_liabilities)

    @classmethod
    def calcualte_debt_ratio(
        cls,
        total_debt: Union[int, float],
        total_assets: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_debt, total_assets)

    @classmethod
    def calcualte_long_term_debt_to_capitalization(
        cls,
        long_term_debt: Union[int, float],
        common_stock: Union[int, float],
    ) -> Union[int, float]:
        long_debt_and_com_stock = long_term_debt + common_stock
        return divide_or_zero(long_term_debt, long_debt_and_com_stock)

    @classmethod
    def calcualte_total_debt_to_capitalization(
        cls,
        total_debt: Union[int, float],
        debt_and_equity: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(total_debt, debt_and_equity)
