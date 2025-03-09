from dataclasses import dataclass


@dataclass
class Account:
    id: int
    uid: str
    email: str
    status: str
