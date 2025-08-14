from langchain_milvus import Milvus
from pymilvus import connections
from pymilvus import utility
from GitHub_Prepared_Rag.Config.config import *
from GitHub_Prepared_Rag.Core.abstraction_base.db_base import BaseVectorDB
class MilvusDB(BaseVectorDB):
    def __init__(self,embedding,config=None):
        super().__init__(embedding,config)
        self.collection_name = self.config['collection_name']
        self.connect()
        self.vector_db = Milvus(
            embedding_function=self.embedding,
            **self.config
        )
    def connect(self):
        if not connections.has_connection(alias=self.config['connection_args']['alias']):
            connections.connect(**self.config['connection_args'])


    def collection_exists(self) -> bool:
        """检查集合是否存在"""
        return utility.has_collection(self.collection_name,
                                      using=self.config['connection_args']['alias']
        )

    def create_collection(self, chunks):
        """创建集合并添加文档（纯数据库操作）"""
        self.vector_db = Milvus.from_documents(
            documents=chunks,
            embedding=self.embedding,
            **self.config
        )
    def add_documents(self,chunks):
        if not self.collection_exists():
            #如果集合不存在
            print("集合不存在,正在创建...")
            self.create_collection(chunks)
            print("创建完毕...")
        else:
            #集合已经存在,但是有两种情况:vectordb初始化和未初始化
            if not self.vector_db:
                self.vector_db = Milvus(
                    embedding_function=self.embedding,
                    **self.config
                )
        self.vector_db.add_documents(chunks)

    def drop_collection(self):
        """删除集合（纯数据库操作）"""
        if self.collection_exists():
            utility.drop_collection(
                collection_name=self.collection_name,
                using=self.config["connection_args"]["alias"]
            )

    def get_retriever(self,**kwargs):
        if not self.vector_db:
            self.vector_db = Milvus(
                embedding_function=self.embedding, **self.config
            )
        return self.vector_db.as_retriever(**kwargs)

    def clear(self):
        connections.disconnect(alias=self.config['connection_args']['alias'])
        print(f"连接{self.config['connection_args']['alias']}已断开")

