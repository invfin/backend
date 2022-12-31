from typing import Union


class FreeCashFlowRatios:
    @classmethod
    def calculate_fcf_equity(
        cls,
        net_cash_provided_by_operating_activities: Union[int, float],
        capital_expenditure: Union[int, float],
        debt_repayment: Union[int, float],
    ) -> Union[int, float]:
        return net_cash_provided_by_operating_activities + capital_expenditure + debt_repayment

    @classmethod
    def calculate_unlevered_fcf(
        cls,
        nopat: Union[int, float],
        depreciation_and_amortization: Union[int, float],
        change_in_working_capital: Union[int, float],
        capital_expenditure: Union[int, float],
    ) -> Union[int, float]:
        return nopat + depreciation_and_amortization + change_in_working_capital + capital_expenditure

    @classmethod
    def calculate_unlevered_fcf_ebit(
        cls,
        operating_income: Union[int, float],
        depreciation_and_amortization: Union[int, float],
        deferred_income_tax: Union[int, float],
        change_in_working_capital: Union[int, float],
        capital_expenditure: Union[int, float],
    ) -> Union[int, float]:
        return (
            operating_income
            + depreciation_and_amortization
            + deferred_income_tax
            + change_in_working_capital
            + capital_expenditure
        )

    @classmethod
    def calculate_owners_earnings(
        cls,
        net_income: Union[int, float],
        depreciation_and_amortization: Union[int, float],
        change_in_working_capital: Union[int, float],
        capital_expenditure: Union[int, float],
    ) -> Union[int, float]:
        return net_income + depreciation_and_amortization + change_in_working_capital + capital_expenditure
