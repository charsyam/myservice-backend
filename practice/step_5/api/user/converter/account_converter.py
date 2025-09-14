from api.user.model.account import Account

class AccountConverter:
    @staticmethod
    def to_dto(entity):
        resp = Account(
            id = entity.id,
            uid = entity.uid,
            email = entity.email,
            status = entity.status,
        ) 

        return resp 
