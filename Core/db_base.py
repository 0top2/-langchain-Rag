from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseVectorDB(ABC):

    @abstractmethod
    def __init__(self, embedding, config):
        self.embedding = embedding
        self.config = config
        self.vector_db = None

    @abstractmethod
    def add_documents(self, docs: List[Document]):
        pass

    @abstractmethod
    def get_retriever(self, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass
