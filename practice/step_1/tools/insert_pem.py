from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64
import pymysql
import sys


# 1️⃣ RSA 키 생성
def generate_rsa_keys():
    key = RSA.generate(2048)  # 2048비트 RSA 키 생성
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def insert_pem(cursor):
    private_key_raw, public_key_raw = generate_rsa_keys()
    private_key = private_key_raw.decode('utf-8')
    public_key = public_key_raw.decode('utf-8')

    query = "insert into certificates values(NULL, %s, %s, 'RSA', 'REGISTERED', now(), now())"

    cursor.execute(query,(public_key, private_key))
    

conn = pymysql.connect(host='127.0.0.1', port=3306, user='insight', passwd='insight', db='shorturl', charset='utf8')

# 커서 가져오기
cursor = conn.cursor()

for i in range(int(sys.argv[1])):
    insert_pem(cursor)

conn.commit()
