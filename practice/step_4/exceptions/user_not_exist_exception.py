from exceptions.base import BaseApiException

class UserNotExistException(BaseApiException):
    def __init__(self, param):
        super().__init__()
        self.param = param 

    def status(self):
        return 404

    def code(self):
        return -10003

    def message(self):
        return f"{self.param} is not existed"
