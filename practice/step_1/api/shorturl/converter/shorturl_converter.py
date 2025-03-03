from api.shorturl.model.shorturl import ShortUrl


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
