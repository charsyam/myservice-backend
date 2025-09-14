from api.shorturl.model.shorturl import ShortUrl, ShortUrlView
from api.shorturl.entity.shorturl import ShortUrl as Entity


class ShortUrlConverter:
    @staticmethod
    def to_dict(entity):
        return {
            "uid": entity.uid,
            "user_id": entity.user_id,
            "user_uid": entity.user_uid,
            "source": entity.source,
            "shorturl": entity.shorturl,
            "status": entity.status,
            "created_at": entity.created_at
        }
        
    @staticmethod
    def to_dto(entity):
        resp = ShortUrlView(
            uid = entity.uid,
            source = entity.source,
            shorturl = entity.shorturl,
            status = entity.status,
            created_at = entity.created_at
        ) 

        return resp 

    @staticmethod
    def to_entity_from_json(value):
        resp = Entity(
            uid = value["uid"],
            user_id = value["user_id"],
            user_uid = value["user_uid"],
            source = value["source"],
            shorturl = value["shorturl"],
            status = value["status"],
            created_at = value["created_at"]
        ) 

        return resp 
