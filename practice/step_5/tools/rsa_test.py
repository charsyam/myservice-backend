from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import pymysql
import sys


# 2️⃣ RSA 공개키로 암호화
def rsa_encrypt(public_key: bytes, message: str) -> str:
    rsa_key = RSA.import_key(public_key)
    cipher = PKCS1_OAEP.new(rsa_key)  # OAEP 패딩 적용
    encrypted_data = cipher.encrypt(message.encode())  # 바이트 변환 후 암호화
    return base64.b64encode(encrypted_data).decode()  # Base64 인코딩 후 반환


# 3️⃣ RSA 개인키로 복호화
def rsa_decrypt(private_key: bytes, encrypted_message: str) -> str:
    rsa_key = RSA.import_key(private_key)
    cipher = PKCS1_OAEP.new(rsa_key)
    encrypted_data = base64.b64decode(encrypted_message)  # Base64 디코딩
    decrypted_data = cipher.decrypt(encrypted_data)  # 복호화
    return decrypted_data.decode()  # 문자열 변환 후 반환


conn = pymysql.connect(host='127.0.0.1', port=3306, user='insight', passwd='insight', db='shorturl', charset='utf8')

# 커서 가져오기
cursor = conn.cursor()

# 🔥 테스트 실행
if __name__ == "__main__":
    cert_id = int(sys.argv[1])

    query = f"select public_key, private_key from certificates where id={cert_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    public_key = result[0]
    private_key = result[1]

    print(public_key)

    public_key_raw = public_key.encode('utf-8')
    private_key_raw = private_key.encode('utf-8')

    encrypted_message = rsa_encrypt(public_key_raw, "message") 
    print(encrypted_message)

    decrypted_message = rsa_decrypt(private_key_raw, encrypted_message)
    print(decrypted_message)
