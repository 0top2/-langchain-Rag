from abc import ABC, abstractmethod
from .db_base import BaseVectorDB

class UpdateStrategy(ABC):
    @abstractmethod
    def execute(self,db:BaseVectorDB,chunks):
        """执行更新逻辑
                :param db: 数据库实例（遵循BaseVectorDB接口）
                :param chunks: 需要更新的文档
        """
        pass