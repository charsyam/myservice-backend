from api.shorturl.model.shorturl import ShortUrl
from api.shorturl.entity.shorturl import ShortUrl as Entity


class ShortUrlConverter:
    @staticmethod
    def to_dto(entity):
        resp = ShortUrl(
            id = entity.id,
            source = entity.source,
            shorturl = entity.shorturl,
            status = entity.status,
        ) 

        return resp 

    @staticmethod
    def to_entity_from_json(value):
        resp = Entity(
            id = value["id"],
            uid = value["uid"],
            user_id = value["user_id"],
            user_uid = value["user_uid"],
            source = value["source"],
            shorturl = value["shorturl"],
            status = value["status"],
            created_at = value["created_at"]
        ) 

        return resp 
