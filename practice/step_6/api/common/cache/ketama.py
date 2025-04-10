import hashlib
import bisect
import mmh3
import redis
import time
from typing import Dict, List


def redis_connector(host, port):
    redis_conn = redis.Redis(host=host, port=port, decode_responses=True)
    return redis_conn


def mmh_hash(key):
    return mmh3.hash(key.encode('utf-8'), 0, False)


def ketama_hash(key: str, alignment: int) -> int:
    """ 
    Ketama 해시 함수 (C 코드와 동일한 동작)
    
    :param key: 해싱할 키 (문자열)
    :param alignment: MD5 결과에서 4바이트(32비트)를 추출하기 위한 인덱스 (0~3)
    :return: 32비트 정수 해시 값
    """
    md5_hash = hashlib.md5(key.encode('utf-8')).digest()  # MD5 해시 (16바이트)

    # C 코드와 동일한 방식으로 특정 4바이트를 추출하여 32비트 정수 변환
    return ((md5_hash[3 + alignment * 4] & 0xFF) << 24) | \
           ((md5_hash[2 + alignment * 4] & 0xFF) << 16) | \
           ((md5_hash[1 + alignment * 4] & 0xFF) << 8) | \
           (md5_hash[0 + alignment * 4] & 0xFF)


def test():
    NUM = 100000
    start = time.time()
    for i in range(NUM):
        mmh_hash("testabcd")
    end = time.time()

    print(f"mmh: {end-start}")

    start = time.time()
    for i in range(NUM):
        ketama_hash("testabcd", 0)
    end = time.time()

    print(f"ketama: {end-start}")



class KatemaConsistentHashing:
    def __init__(self, hosts: List, connector=redis_connector, key_hash=mmh_hash, distributed_hash=ketama_hash, num_replicas: int = 160):
        """
        Redis를 활용한 Ketama Consistent Hashing 구현
        :param num_replicas: 각 Redis 노드당 가상 노드 개수 (기본값: 160)
        """
        self.num_replicas = num_replicas
        self.ring = {}
        self.sorted_keys = []
        self.nodes = {}
        self.distributed_hash = distributed_hash
        self.key_hash = key_hash or distributed_hash
        self.connector = connector

        for host in hosts:
            self.add_node(host[0], host[1], host[2])
    
    def add_node(self, host: str, port: int, node_name: str = None):
        if not node_name:
            node_name = f"{host}:{port}"

        """Redis 노드를 추가하고 가상 노드를 생성하여 배치"""
        if node_name in self.nodes:
            return  # 중복 추가 방지

        conn = self.connector(host, port)
        self.nodes[node_name] = conn

        for i in range(self.num_replicas):
            virtual_node = f"{node_name}#{i}"
            alignment = i // 40
            key = self.distributed_hash(virtual_node, alignment)
            self.ring[key] = node_name
            bisect.insort(self.sorted_keys, key)

    def remove_node(self, node_name: str):
        """노드를 제거하고 가상 노드 삭제"""
        if node_name not in self.nodes:
            return

        del self.nodes[node_name]  # Redis 연결 제거

        for i in range(self.num_replicas):
            virtual_node = f"{node_name}#{i}"
            alignment = i // 40
            key = self.distributed_hash(virtual_node, alignment)
            if key in self.ring:
                del self.ring[key]
                self.sorted_keys.remove(key)

    def get_node_name(self, key: str):
        """키에 대해 담당할 Redis 노드 찾기"""
        if not self.ring:
            return None

        key_hash = self.key_hash(key)
        idx = bisect.bisect(self.sorted_keys, key_hash) % len(self.sorted_keys)
        return self.ring[self.sorted_keys[idx]]

    def get_node(self, key: str):
        node_name = self.get_node_name(key)
        if node_name and node_name in self.nodes:
            return self.nodes[node_name]

        raise Exception("No Consistent Hash Node")
        

    def get_ring(self) -> Dict[int, str]:
        """현재 해시 링 상태 반환"""
        return {k: self.ring[k] for k in self.sorted_keys}


def cache_set(ch, key, value):
    ch.get_node(key).set(key, value)

def cache_get(ch, key):
    return ch.get_node(key).get(key)

# 테스트 코드
if __name__ == "__main__":
    hosts = [
        ("127.0.0.1", 6379, "Redis1"),
    ]
    ch = KatemaConsistentHashing(hosts=hosts, connector=redis_connector)
    
    # Redis 서버 추가 (실제 실행 전, Redis 서버가 실행 중이어야 함)
#    ch.add_node("Redis1", "127.0.0.1", 6379)
#    ch.add_node("Redis2", "127.0.0.1", 6380)
#    ch.add_node("Redis3", "127.0.0.1", 6381)

    ch.add_node("127.0.0.1", 6380, "Redis2")
    ch.add_node("127.0.0.1", 6381, "Redis3")
    # 키-값 저장

    cache_set(ch, "apple", "🍎")
    cache_set(ch, "banana", "🍌")
    cache_set(ch, "cherry", "🍒")
    cache_set(ch, "date", "🌴")
    cache_set(ch, "elderberry", "🍇")

    # 키-값 조회
    print(cache_get(ch, "apple"))
    print(cache_get(ch, "banana"))
    print(cache_get(ch, "cherry"))

    # Redis 노드 제거 후 테스트
    print("\n🔴 Redis2 제거 후:")
    ch.remove_node("Redis2")

    print(cache_get(ch, "apple"))
    print(cache_get(ch, "banana"))

    test()
