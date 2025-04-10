from abc import ABC, abstractmethod


class Worker(ABC):
    def match(self, event):
        return False

    @abstractmethod
    def process(self, item):
        pass

    @abstractmethod
    def event_type(self):
        pass
