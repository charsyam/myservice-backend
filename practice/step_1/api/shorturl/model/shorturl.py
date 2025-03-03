from dataclasses import dataclass


@dataclass
class ShortUrl:
    id: int
    source: str
    shorturl: str
    status: str
