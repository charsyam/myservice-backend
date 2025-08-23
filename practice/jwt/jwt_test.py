import jwt
import datetime


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


# 3. JWT 검증(서명 확인)
def verify_jwt(token):
    try:
        # HS256 검증(비밀키로 확인)
        decoded_payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_payload
    except jwt.ExpiredSignatureError:
        return "- 토큰이 만료되었습니다!"
    except jwt.InvalidTokenError:
        return "- 잘못된 토큰입니다!"


# 실행 예제
if __name__ == "__main__":
    token = create_jwt()
    print(f"+ 생성된 JWT: {token}\n")


    decoded_data = verify_jwt(token)
    print(f"+ 검증 결과: {decoded_data}")
