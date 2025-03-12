import redis

redis_pool = redis.ConnectionPool(host='127.0.0.11', port=6379, db=0, max_connections=4)

def get_redis_conn():
    return redis.StrictRedis(connection_pool=redis_pool)
