class ArgsAndKwargsExcpetion(Exception):
    """Exception raised when args and kwargs are passed at the same time
    Attributes:
        message -- explanation of the error
    """
    def __init__(self):
        self.message = "To use custom values for the model use either ars or kwargs but not both"
        super().__init__(self.message)
