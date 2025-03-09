import logging
import json
from pythonjsonlogger import jsonlogger

from api.common.session_vars import session_context


LOG_FILE = "./shorturl.log"

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(name)s %(message)s %(filename)s %(lineno)d"
)


logging.getLogger("uvicorn.access").disabled = True
logging.getLogger("uvicorn.error").disabled = True

handler = logging.FileHandler(LOG_FILE)
#handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class ContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord):
        return True
