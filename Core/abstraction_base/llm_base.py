from abc import ABC, abstractmethod
class LLM(ABC):
    @abstractmethod
    def create_llm(self,config):
        pass