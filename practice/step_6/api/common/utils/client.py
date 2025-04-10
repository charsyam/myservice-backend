from fastapi import Request


def get_client_ip(request: Request):
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        # 여러 IP가 있을 수 있으므로 첫 번째 IP를 사용
        client_ip = forwarded_for.split(",")[0]
    else:
        # 프록시가 없을 경우 클라이언트 IP
        client_ip = request.client.host

    return client_ip
