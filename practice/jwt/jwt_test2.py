import jwt
import datetime
import hmac
import hashlib
import base64


# 1. 비밀키 설정(대칭키)
SECRET_KEY = "insight_api_secret_key"


# 2. JWT 생성(서명 포함)
def create_jwt():
    payload = {
        "user_id": "1",  # 유저 ID
        "user_uid": "18d4e9b9-c149-467e-885d-a12352e52810",
        "name": "clark",  # 사용자 이름
        "iat": datetime.datetime.utcnow(),  # 발급 시간
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # 만료 시간 (1시간)
    }


    # JWT 생성(HS256 서명)
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token


# 3. 수동으로 서명 생성(HMAC-SHA256)
def generate_hmac_signature(header, payload, secret_key):
    # Base64Url 인코딩된 Header + Payload
    message = f"{header}.{payload}"


    # HMAC-SHA256 서명 생성
    signature = hmac.new(secret_key.encode(), message.encode(), hashlib.sha256).digest()


    # Base64Url 인코딩하여 최종 서명 생성
    signature_b64url = base64.urlsafe_b64encode(signature).decode().rstrip("=")  # 패딩 제거


    return signature_b64url


# 4. JWT 검증(Signature 부분 직접 검증)
def verify_jwt(token):
    try:
        # JWT를 헤더, 정보, 서명으로 분리
        header_b64, payload_b64, signature_b64 = token.split(".")


        # 수동으로 서명 생성
        expected_signature = generate_hmac_signature(header_b64, payload_b64, SECRET_KEY)


        # PyJWT를 사용하여 검증(기본 검증)
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])


        # 서명이 동일한지 확인
        if signature_b64 == expected_signature:
            return {"+ 검증 성공": decoded_payload}
        else:
            return {"- 서명 불일치": "변조된 토큰!"}


    except jwt.ExpiredSignatureError:
        return {"- 토큰이 만료되었습니다!"}
    except jwt.InvalidTokenError:
        return {"- 잘못된 토큰입니다!"}


# 실행 예제
if __name__ == "__main__":
    token = create_jwt()
    print(f"+ 생성된 JWT: {token}\n")


    decoded_data = verify_jwt(token)
    print(f"+ 검증 결과: {decoded_data}")
