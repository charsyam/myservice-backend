import base64
import pymysql
import sys
import uuid
import copy

STEP = 10000

TEMPLATE = "insert into shorturls(id, uid, user_id, user_uid, source, shorturl, status, created_at) values "

def insert_shorturl(cursor, count):
    for i in range(count):
        arr = []
        for j in range(STEP):
            value = f"(NULL, '{uuid.uuid4()}', 1, '66eb7036-0d24-4c2a-9451-fe966699515d', 'https://www.naver.com', '{uuid.uuid4()}', 'REGISTERED', now())"
            arr.append(value)

        sub_str = ','.join(arr)

        query = TEMPLATE + sub_str
        cursor.execute(query)
        conn.commit()
    

conn = pymysql.connect(host='127.0.0.1', port=3306, user='insight', passwd='insight', db='shorturl', charset='utf8')

# 커서 가져오기
cursor = conn.cursor()

count = int(sys.argv[1])
insert_shorturl(cursor, count)

