from dataclasses import dataclass


@dataclass
class Item:
    item_type: str
    params: dict
