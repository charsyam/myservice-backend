from dataclasses import dataclass
from datetime import datetime


@dataclass
class Token:
    id: int
    uid: str
    access_token: str
    refresh_token: str
    status: str
    created_at: datetime
