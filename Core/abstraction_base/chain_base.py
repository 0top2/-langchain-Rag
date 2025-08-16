from abc import ABC, abstractmethod

class ChainBase(ABC):
    @abstractmethod
    def build_chain(self):
        pass