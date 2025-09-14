from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel
from typing import Any, Dict


class Response(BaseModel):
    header: Dict[str, Any] = {}
    body: Dict[str, Any] = {}
