from api.auth.model.certificate import Certificate

class CertificateConverter:
    @staticmethod
    def to_dto(entity):
        resp = Certificate(
            id = entity.id,
            public_key = entity.public_key,
            encrypt_type = entity.encrypt_type,
            status = entity.status,
        ) 

        return resp 
