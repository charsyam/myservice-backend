from exceptions.base import BaseApiException

class PasswordMismatchException(BaseApiException):
    def __init__(self, email):
        super().__init__()
        self.email = email

    def code(self):
        return -10004

    def message(self):
        return f"{self.email}'s password is not valid"
