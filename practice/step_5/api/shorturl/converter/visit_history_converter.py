from api.shorturl.model.visit_history import VisitHistory


class VisitHistoryConverter:
    @staticmethod
    def to_dao(entity):
        resp = {
            id = entity.id,
            uid = entity.uid,
            shorturl_id = entity.shorturl_id,
            shorturl_uid = entity.shorturl_uid,
            agent = entity.agent,
            request_ip = entity.request_ip,
            status = entity.status,
            created_at = entity.created_at
        }

        return resp
