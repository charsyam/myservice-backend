class BaseApiException(Exception):
    def __init__(self):
        pass 

    def status(self):
        return 500

    def code(self):
        return -100

    def message(self):
        return ""
