from dataclasses import dataclass
from datetime import datetime


@dataclass
class ShortUrlView:
    uid: str
    source: str
    shorturl: str
    status: str
    created_at: datetime


@dataclass
class ShortUrl:
    uid: str
    user_id: int
    user_uid: str
    source: str
    shorturl: str
    status: str
    created_at: datetime
