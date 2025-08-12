from langchain_milvus import Milvus
from pymilvus import connections
from pymilvus import utility
from GitHub_Prepared_Rag.Config.config import *
from GitHub_Prepared_Rag.Core.db_base import BaseVectorDB
class MilvusDB(BaseVectorDB):
    def __init__(self,embedding,config=None):
        super().__init__(embedding,config)
        self.collection_name = self.config['collection_name']
        self.embedding = embedding
        self.vector_db = None
        self._connect()
    def _connect(self):
        if not connections.has_connection(alias=self.config['connection_args']['alias']):
            connections.connect(**milvus_config['connection_args'])


    def _collection_exists(self) -> bool:
        """检查集合是否存在"""
        return utility.has_collection(self.collection_name,using=self.config['connection_args']['alias'])


    def add_documents(self,docs):
        if not self._collection_exists():
            self.vector_db = Milvus.from_documents(
                documents=docs,
                embedding=self.embedding,
                **self.config
        )
        else:
            update = input("是否需要更新数据库(Y/N):")
            if update in ["Y","y"]:
                # 删除现有集合
                utility.drop_collection(collection_name=self.collection_name,using=self.milvus_config['connection_args']['alias'])
                print(f"已删除集合 '{self.collection_name}'")
                self.vector_db = Milvus.from_documents(
                                    documents=docs,
                                    embedding=self.embedding,
                                    **self.config
                                    )
            elif update in ["N","n"]:
                self.vector_db = Milvus(embedding_function=self.embedding,**self.config)

    def get_retriever(self,**kwargs):
        if not self.vector_db:
            # 规范异常抛出（使用Exception类），明确错误原因
            raise Exception("向量数据库未初始化，请先调用handle_db方法创建/连接集合")
        return self.vector_db.as_retriever(**kwargs)

    def clear(self):
        connections.disconnect(alias=self.config['connection_args']['alias'])
        print(f"连接{self.config['connection_args']['alias']}已断开")

