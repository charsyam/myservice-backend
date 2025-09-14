from api.auth.repository.certificate_repository import CertificateRepository
from api.auth.converter.certificate_converter import CertificateConverter
import random


class CertificateService:
    def __init__(self, db):
        self.repository = CertificateRepository(db)

    def get_one_certificate(self):
        count = self.repository.count_all()

        certificate_id = random.randrange(1, count+1)
        entity = self.repository.find_by_id(certificate_id)
        if not entity:
            raise CertificateNotExistException(certificate_id)

        return CertificateConverter.to_dto(entity)

    def get_private_key(self, certificate_id) -> str:
        entity = self.repository.find_by_id(certificate_id)
        if not entity:
            raise CertificateNotExistException(certificate_id)
        
        return entity.private_key.encode('utf-8')
