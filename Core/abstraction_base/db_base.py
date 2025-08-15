from abc import ABC, abstractmethod
from typing import List
from langchain_core.documents import Document

class BaseVectorDB(ABC):

    @abstractmethod
    def __init__(self, embedding, config):
        self.embedding = embedding
        self.config = config
        self.vector_db = None
        self._initialize()

    @abstractmethod
    def _initialize(self):
        '''根据不同数据库的逻辑进行一些初始化操作,使其接下来可以进行CRUD操作'''
        pass


    @abstractmethod
    def add_documents(self, docs: List[Document]):
        pass

    @abstractmethod
    def clear_documents(self):
        pass

    @abstractmethod
    def get_retriever(self, **kwargs):
        pass

    @abstractmethod
    def clear(self):
        pass
