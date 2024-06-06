"""General exceptions"""


class FailedToPredictException(Exception):
    """Exception for when the model can not predict something"""

    def __init__(
        self,
        message: str,
    ) -> None:
        self.message = message
        super().__init__(self.message)
