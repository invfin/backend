from typing import Union


from .utils import divide_or_zero


class ValuationRatios:
    @classmethod
    def calculate_price_to_book(
        cls,
        current_price: Union[int, float],
        book_value_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, book_value_per_share)

    @classmethod
    def calculate_price_to_cash(
        cls,
        current_price: Union[int, float],
        cash_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, cash_per_share)

    @classmethod
    def calculate_price_to_earnings(
        cls,
        current_price: Union[int, float],
        earnings_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, earnings_per_share)

    @classmethod
    def calculate_price_to_earnings_growth(
        cls,
        price_to_earnings: Union[int, float],
        net_income_growth: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(price_to_earnings, net_income_growth).real

    @classmethod
    def calculate_price_to_sales(
        cls,
        current_price: Union[int, float],
        sales_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, sales_per_share)

    @classmethod
    def calculate_price_to_total_assets(
        cls,
        current_price: Union[int, float],
        total_assets_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, total_assets_per_share)

    @classmethod
    def calculate_price_to_fcf(
        cls,
        current_price: Union[int, float],
        free_cashflow_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, free_cashflow_per_share)

    @classmethod
    def calculate_price_to_operating_cf(
        cls,
        current_price: Union[int, float],
        operating_cashflow_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, operating_cashflow_per_share)

    @classmethod
    def calculate_price_to_tangible_assets(
        cls,
        current_price: Union[int, float],
        tangible_assets_per_share: Union[int, float],
    ) -> Union[int, float]:
        return divide_or_zero(current_price, tangible_assets_per_share)
