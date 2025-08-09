from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from GitHub_Prepared_Rag.Config.config import *
from .llm_utils import llm
from .embedding_utils import embedding
from .document_utils import *
from .retriever_utils import *
from GitHub_Prepared_Rag.Utils.format_doc import format_doc
from GitHub_Prepared_Rag.Utils.Milvus_utils import MilvusOperator


class RagManager:
    def __init__(self):
        self.embedding = embedding()  #可以在embedding参数指定模型名
        self.documents = load_doc()
        self.chunk = split_doc(self.documents,self.embedding)
        self.llm = llm()
        self.milvus = MilvusOperator(self.embedding)
        self.milvus.handle_db(self.documents)
        self.db = self.milvus.vector_db
        self.retriever = None
        self.prompt = ChatPromptTemplate.from_messages([
            ('system', '你是一个专业的文档信息解读专家,请你根据文档里的内容和历史记录并结合一些常识来回答用户的问题,不用过于严谨,只输出答案,不要多余内容'
                       '文档内容:`{context}`'

                       '历史记录:`{history}`'),
            ('user', '{input}')
        ])
    def get_retriever(self):
        return query_rewrite_retriever(Retriever(self.db.as_retriever(), self.chunk), self.llm)
    def get_async_retriever(self):
        return Retriever(self.db.as_retriever(), self.chunk)
    def get_info(self):
        return self.llm, self.embedding
