from abc import ABC, abstractmethod
from typing import List


class Subscriber(ABC):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify(self, docs):
        for observer in self.observers:
            observer.update(docs)

class Observer(ABC):
    @abstractmethod
    def update(self, docs, strategy=None):
        '''接收文档变更并执行自己的相应逻辑(如更新嵌入等)'''
        pass
