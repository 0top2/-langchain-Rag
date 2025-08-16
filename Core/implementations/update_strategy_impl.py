from GitHub_Prepared_Rag.Core.abstraction_base.db_base import BaseVectorDB
from GitHub_Prepared_Rag.Core.abstraction_base.update_strategy_base import UpdateStrategy

class AppendStrategy(UpdateStrategy):
    def execute(self,db:BaseVectorDB,new_chunks):
        db.add_documents(new_chunks)


class DropAndRecreateStrategy(UpdateStrategy):
    def execute(self,db:BaseVectorDB,whole_chunks):
        db.drop_collection()
        db.create_collection(whole_chunks)

class NoUpdateStrategy(UpdateStrategy):
    def execute(self, db: BaseVectorDB, chunks):
        print("启动时未进行更新，数据库保持原有状态")