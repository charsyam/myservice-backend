from exceptions.base import BaseApiException

class UserAlreadyExistException(BaseApiException):
    def __init__(self, email):
        super().__init__()
        self.email = email

    def code(self):
        return -10001

    def message(self):
        return f"{self.email} is already existed"
