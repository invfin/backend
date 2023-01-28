from typing import Union


def calculate_compound_growth(
    numerator: Union[int, float],
    denominator: Union[int, float],
    years: int,
) -> Union[int, float]:
    return ((divide_or_zero(numerator, denominator) ** (1 / years)) - 1) * 100


def modify_for_percentage(value: Union[int, float], as_percentage: bool = True) -> Union[int, float]:
    return round(value * 100, 2) if as_percentage else value


def divide_or_zero(
    numerator: Union[int, float, complex],
    denominator: Union[int, float, complex],
    numbers_after_coma: int = 2,
) -> Union[int, float]:
    """A method to calculate a division that returns de product or 0 if the denominator is 0

    Parameters
    ----------
    numerator : Union[int, float]
        The numerator of the division
    denominator : Union[int, float]
        The denominator of the division
    numbers_after_coma: int
        The number of values after the coma

    Returns
    -------
    Union[int, float]
        The product of the division
    """
    try:
        return round((numerator / denominator).real, numbers_after_coma)
    except ZeroDivisionError:
        return 0
