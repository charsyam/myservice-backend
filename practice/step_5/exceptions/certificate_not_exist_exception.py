from exceptions.base import BaseApiException

class CertificateNotExistException(BaseApiException):
    def __init__(self, param):
        super().__init__()
        self.param = param 

    def code(self):
        return -10201

    def status(self):
        return 404

    def message(self):
        return f"{self.param} is not existed"
