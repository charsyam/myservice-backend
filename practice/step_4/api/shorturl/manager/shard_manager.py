from dataclasses import dataclass
import mmh3

from database import get_shorturl_shard_session
from exceptions import *


@dataclass
class ShardInfo:
    start: int
    end: int
    shard_id: int
    

def binary_search(array, key, start, end):
    if start > end:
        return None

    mid = (start + end) // 2
    
    if key >= array[mid].start and key < array[mid].end:
        return mid

    elif key < array[mid].start:
        return binary_search(array, key, start, mid-1)

    else:
        return binary_search(array, key, mid+1, end)



class ShortUrlShardManager:
    def __init__(self, mappings, max_logical_shard_count = 16384):
        self.mappings = mappings
        self.max_logical_shard_count = max_logical_shard_count
        self.used_sessions = {}

    def get_physical_shard_id(self, shard_id):
        idx = binary_search(self.mappings, shard_id, 0, len(self.mappings))
        if idx == None:
            raise InvalidParameterException(f"shard_id is {shard_id}")

        return self.mappings[idx].shard_id

    def get_logical_shard_id(self, url):
        return mmh3.hash(url) % self.max_logical_shard_count

    def get_shard(self, url):
        logical_shard_id = self.get_logical_shard_id(url)
        physical_shard_id = self.get_physical_shard_id(logical_shard_id)

        session = None
        if physical_shard_id in self.used_sessions:
            session = self.used_sessions[physical_shard_id]
        else:
            session = get_shorturl_shard_session(physical_shard_id).__next__()
            self.used_sessions[physical_shard_id] = session

        return session

    def commit(self):
        for key in self.used_sessions.keys(): 
            self.used_sessions[key].commit()


    def rollback(self):
        for key in self.used_sessions.keys(): 
            self.used_sessions[key].rollback()
        
          
mappings = [
    ShardInfo(0, 8000, 0),
    ShardInfo(8000, 16384, 1),
]


def get_shard_manager():
    return ShortUrlShardManager(mappings)
