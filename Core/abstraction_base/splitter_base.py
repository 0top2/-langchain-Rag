from abc import ABC , abstractmethod


class SplitterBase(ABC):
    @abstractmethod
    def split(self, docs,embedding):
        '''分块的核心方法'''
        pass