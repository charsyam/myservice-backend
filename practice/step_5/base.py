class BaseApiException(Exception):
    def status(self):
        return 500

    def code(self):
        return -100

    def message(self):
        return ""
