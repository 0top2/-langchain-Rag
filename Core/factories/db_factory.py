from GitHub_Prepared_Rag.Core.implementations.db_milvus import MilvusDB
from GitHub_Prepared_Rag.Config.config import *

class DBFactory:

    @staticmethod
    def create_db(embedding):
        if Database == 'milvus':
            return MilvusDB(embedding,milvus_config)

        else:
            raise ValueError(f"不支持的数据库类型: {Database}")
