class TickerNotFound(Exception):
    """
    Exception raised for lang parameter.
    Attributes
    ----------
        ticker: str
            The ticker of the company
        message: str
            explanation of the error
    """

    def __init__(self, ticker: str, message: str = "Quote not found for ticker symbol:"):
        self.ticker = ticker
        self.message = f"{message} {ticker}"
        super().__init__(self.message)
