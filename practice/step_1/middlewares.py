from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import *

import traceback
import time


def create_middlewares(app: FastAPI):
    @app.middleware("http")
    async def custom_middleware_exception_handler(request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except BaseApiException as e:
            print(traceback.format_exc())
            return JSONResponse(
                status_code=e.status(),
                content={"header": {"code": e.code(), "message": e.message()}, "body": {}}
            )
        except Exception as e:
            print(traceback.format_exc())
            return JSONResponse(
                status_code=500,
                content={"header": {"code": -100, "message": str(e)}, "body": {}}
            )

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)

        return response
