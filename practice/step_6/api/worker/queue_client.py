from abc import ABC, abstractmethod

class QueueClient(ABC):
    @abstractmethod
    def push(self, key, value):
        pass

    
    @abstractmethod
    def pop(self, key):
        pass
