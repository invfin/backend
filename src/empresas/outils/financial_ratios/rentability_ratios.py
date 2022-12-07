from typing import Union


from .utils import divide_or_zero, modify_for_percentage


class RentabilityRatios:
    @classmethod
    def calculate_roa(
        cls,
        net_income: Union[int, float],
        total_assets: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(net_income, total_assets)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_roe(
        cls,
        net_income: Union[int, float],
        total_stockholders_equity: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(net_income, total_stockholders_equity)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_roc(
        cls,
        operating_income: Union[int, float],
        total_assets: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(operating_income, total_assets)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_roce(
        cls,
        operating_income: Union[int, float],
        capital_employed: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(operating_income, capital_employed)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_rota(
        cls,
        net_income: Union[int, float],
        tangible_assets: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(net_income, tangible_assets)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_roic(
        cls,
        net_income: Union[int, float],
        dividends_paid: Union[int, float],
        invested_capital: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero((net_income - dividends_paid), invested_capital)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_nopat_roic(
        cls,
        nopat: Union[int, float],
        invested_capital: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(nopat, invested_capital)
        return modify_for_percentage(result, as_percentage)

    @classmethod
    def calculate_rogic(
        cls,
        nopat: Union[int, float],
        gross_invested_capital: Union[int, float],
        as_percentage: bool = True,
    ) -> Union[int, float]:
        result = divide_or_zero(nopat, gross_invested_capital)
        return modify_for_percentage(result, as_percentage)
