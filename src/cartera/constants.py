from enum import Enum


class InvestmentMovement(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    RECEIVE_FUND = "RECEIVE_FUND"
    SEND_FUND = "SEND_FUND"

    @classmethod
    def to_choices(cls):
        return ((m.value, m.value.lower()) for m in cls)
