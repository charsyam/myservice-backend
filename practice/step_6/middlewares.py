from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import *

import traceback
import time
import uuid

from api.common.session_vars import session_context
from api.common.logger import logger


X_TRANSACTION_ID = "x-transaction-id"


def create_middlewares(app: FastAPI):
    @app.middleware("http")
    async def custom_middleware_exception_handler(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseApiException as e:
            return JSONResponse(
                status_code=e.status(),
                content={"header": {"code": e.code(), "message": e.message()}, "body": {}}
            )
        except Exception as e:
            logger.error(e)
            return JSONResponse(
                status_code=500,
                content={"header": {"code": -100, "message": str(e)}, "body": {}}
            )

    @app.middleware("http")
    async def add_process_header(request: Request, call_next):
        if X_TRANSACTION_ID not in request.headers:
            session_context.get()[X_TRANSACTION_ID] = str(uuid.uuid4())
        else:
            session_context.get()[X_TRANSACTION_ID] = request.headers[X_TRANSACTION_ID]

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["x-process-time"] = str(process_time)
        response.headers[X_TRANSACTION_ID] = session_context.get()[X_TRANSACTION_ID]
        logger.info(request.url, extra={"process_time": str(process_time)})

        return response
