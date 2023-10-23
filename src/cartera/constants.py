from enum import Enum


class InvestmentMovement(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

    @classmethod
    def to_choices(cls):
        return ((m.value, m.value.lower()) for m in cls)
