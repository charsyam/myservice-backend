import logging
import json
from pythonjsonlogger import jsonlogger

from api.common.session_vars import session_context


handler = logging.StreamHandler()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)
