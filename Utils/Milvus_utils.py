from langchain_milvus import Milvus
from pymilvus import connections
from pymilvus import utility
from GitHub_Prepared_Rag.Config.config import *

class MilvusOperator:
    def __init__(self,embedding):
        self.collection_name = milvus_config['collection_name']
        self.milvus_config = {
            "collection_name": self.collection_name,
            "connection_args": {
                "host": milvus_config['connection_args']['host'],
                "port": milvus_config['connection_args']['port'],
                "user": milvus_config['connection_args']['user'],
                "password": milvus_config['connection_args']['password'],
                "db_name": milvus_config['connection_args']['db_name'],
                "alias": milvus_config['connection_args']['alias'],
            },
            # 高级参数（可选）
            "index_params": {
                "index_type": milvus_config['index_params']['index_type'],
                "metric_type": milvus_config['index_params']['metric_type'],  # 余弦相似度
                "params": {"nlist": milvus_config['index_params']['params']['nlist']},
            },
            "search_params": {
                "nprobe": milvus_config['search_params']['nprobe']  # 搜索精度
            },
            "consistency_level": milvus_config['consistency_level'],
            "enable_dynamic_field": True
        }
        self.embedding = embedding
        self.vector_db = None

    def get_fresh_connection(self):
        if connections.has_connection(alias=self.milvus_config['connection_args']['alias']):
            print(f"连接{self.milvus_config['connection_args']['alias']}已存在!")
            return
        connections.connect(**milvus_config['connection_args'])
        print(f"已创建Milvus数据库连接(alias={self.milvus_config['connection_args']['alias']})")

    def _collection_exists(self) -> bool:
        """检查集合是否存在"""
        return utility.has_collection(self.collection_name,using=self.milvus_config['connection_args']['alias'])


    def handle_db(self,docs):
        self.get_fresh_connection()
        if not self._collection_exists():
            self.vector_db = Milvus.from_documents(
                documents=docs,
                embedding=self.embedding,
                **self.milvus_config
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
                                    **self.milvus_config
                                    )
            elif update in ["N","n"]:
                self.vector_db = Milvus(embedding_function=self.embedding,**self.milvus_config)

    def get_retriever(self,**kwargs):
        if not self.vector_db:
            # 规范异常抛出（使用Exception类），明确错误原因
            raise Exception("向量数据库未初始化，请先调用handle_db方法创建/连接集合")
        return self.vector_db.as_retriever(**kwargs)

    def clear(self):
        connections.disconnect(alias=self.milvus_config['connection_args']['alias'])
        print(f"连接{self.milvus_config['connection_args']['alias']}已断开")

