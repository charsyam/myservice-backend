from exceptions.base import BaseApiException

class ExpiredTokenException(BaseApiException):
    def __init__(self, param):
        super().__init__()
        self.param = param

    def code(self):
        return -10010

    def status(self):
        return 401

    def message(self):
        return f"{self.param}"
