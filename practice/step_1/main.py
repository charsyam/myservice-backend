from typing import List, Dict, Any
from prometheus_fastapi_instrumentator import Instrumentator

from fastapi import FastAPI, Depends, Path, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from database import engineconn
from sqlalchemy import func

import random
import uuid

from middlewares import create_middlewares
from api.auth.controller.auth_controller import router as auth_routers
from api.user.controller.user_controller import router as user_routers
from api.shorturl.controller.shorturl_controller import router as shorturl_routers


app = FastAPI()
Instrumentator().instrument(app).expose(app)

create_middlewares(app)


app.include_router(auth_routers)
app.include_router(user_routers)
app.include_router(shorturl_routers)
