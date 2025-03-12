from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import *

import traceback
import time
import uuid
from prometheus_client import Counter

from api.common.session_vars import session_context
from api.common.logger import logger


X_TRACE_ID = "x-trace-id"


exception_counter = Counter(
    "fastapi_exceptions_total",
    "Total number of exceptions by type",
    ["exception_type", "exception_code"]
)


def add_exception_counter(exc, exception_code):
    exception_name = type(exc).__name__ 
    exception_counter.labels(exception_type=exception_name, exception_code=exception_code).inc() 


def create_middlewares(app: FastAPI):
    @app.middleware("http")
    async def custom_middleware_exception_handler(request: Request, call_next):
        extra = {}
        extra[X_TRACE_ID] = session_context.get()[X_TRACE_ID]

        try:
            response = await call_next(request)
            return response
        except BaseApiException as e:
            add_exception_counter(e, e.code()) 
            return JSONResponse(
                status_code=e.status(),
                content={"header": {"code": e.code(), "message": e.message()}, "body": {}}
            )
        except Exception as e:
            #print(traceback.format_exc())
            add_exception_counter(e, -100)
            return JSONResponse(
                status_code=500,
                content={"header": {"code": -100, "message": str(e)}, "body": {}}
            )

    @app.middleware("http")
    async def add_process_header(request: Request, call_next):
        extra = {}
        if X_TRACE_ID not in request.headers:
            session_context.get()[X_TRACE_ID] = str(uuid.uuid4())
        else:
            session_context.get()[X_TRACE_ID] = request.headers[X_TRACE_ID]

        extra["type"] = "request"
        extra[X_TRACE_ID] = session_context.get()[X_TRACE_ID]
        logger.info(request.__dict__, extra=extra)

        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["x-process-time"] = str(process_time)
        response.headers[X_TRACE_ID] = session_context.get()[X_TRACE_ID]
        logger.info(response.__dict__, extra=extra)

        return response
