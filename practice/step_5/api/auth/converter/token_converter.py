from api.auth.model.token import Token

class TokenConverter:
    @staticmethod
    def to_dto(entity):
        resp = Token(
            id = entity.id,
            uid = entity.uid,
            access_token = entity.access_token,
            refresh_token = entity.refresh_token,
            status = entity.status,
            created_at = entity.created_at,
        ) 

        return resp 
