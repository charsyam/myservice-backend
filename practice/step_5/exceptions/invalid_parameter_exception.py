from exceptions.base import BaseApiException

class InvalidParameterException(BaseApiException):
    def __init__(self, param):
        super().__init__()
        self.param = param

    def code(self):
        return -10002

    def message(self):
        return f"{self.param} is invalid"
