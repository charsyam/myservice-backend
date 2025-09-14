from datetime import datetime
from sqlalchemy import inspect


def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in inspect(row).attrs.keys()}


def json_serializer(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # 또는 obj.strftime("%Y-%m-%d %H:%M:%S")
    raise TypeError("Type not serializable")
