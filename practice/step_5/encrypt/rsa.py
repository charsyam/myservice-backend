from Crypto.PublicKey import RSA as RSAi
from Crypto.Cipher import PKCS1_OAEP
import base64


class RSA:
    @staticmethod
    def encrypt(public_key: bytes, message: str) -> str:
        rsa_key = RSAi.import_key(public_key)
        cipher = PKCS1_OAEP.new(rsa_key)  # OAEP 패딩 적용
        encrypted_data = cipher.encrypt(message.encode())  # 바이트 변환 후 암호화
        return base64.b64encode(encrypted_data).decode()  # Base64 인코딩 후 반환

    @staticmethod
    def decrypt(private_key: bytes, encrypted_message: str) -> str:
        rsa_key = RSAi.import_key(private_key)
        cipher = PKCS1_OAEP.new(rsa_key)
        encrypted_data = base64.b64decode(encrypted_message)  # Base64 디코딩
        decrypted_data = cipher.decrypt(encrypted_data)  # 복호화
        return decrypted_data.decode()  # 문자열 변환 후 반환
