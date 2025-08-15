from langchain_core.prompts import ChatPromptTemplate
from GitHub_Prepared_Rag.Core.factories.llm_factory import *
from GitHub_Prepared_Rag.Core.embedding_utils import embedding
from .document_utils import *
from GitHub_Prepared_Rag.Core.factories.db_factory import DBFactory
from GitHub_Prepared_Rag.Core.factories.update_strategy_factory import StrategyFactory
from GitHub_Prepared_Rag.Core.factories.splitter_factory import SplitterFactory
from GitHub_Prepared_Rag.Core.factories.retriever_factory import RetrieverFactory
from .observe_pattern import Observer
from .factories.DocWatcher_updated_factory import DocWatcherUpdatedFactory
class RagManager(Observer):
    def __init__(self):
        self.embedding = embedding()
        self.documents = load_doc()
        self.llm = LLMFactory.create_llm()
        self.db = DBFactory.create_db(self.embedding)
        self.update_strategy = StrategyFactory.create_strategy()

        self.splitter = SplitterFactory.create_splitter()
#不采用self.chunk长期维护一个实例变量,而是创建函数变量,在函数结束时回收,节省空间(尤其是文档过大的情况)
        initial_chunks = self.splitter.split(self.documents,self.embedding)
        self.update_strategy.execute(self.db, initial_chunks)

        self.prompt = ChatPromptTemplate.from_messages([
            ('system', '''你是一个文档问答助手，不具备其他虚构身份,你需要严格按照以下规则回答问题：
                        1. 优先使用提供的文档内容（`{context}`）结合实际常识作为回答依据，确保信息准确。
                        2. 结合对话历史（`{history}`）理解用户意图，保持回答的连贯性。
                        3. 若文档中没有相关信息，可基于常识简要回答，但需注明“文档中未提及相关内容”。
                        4. 语言简洁明了，直接回应用户问题，避免冗余表述。
                       '文档内容:`{context}`'

                       '历史记录:`{history}`
                       '''),
            ('user', '{input}')
        ])
    def update(self,docs,pattern):
        self.documents = docs #有可能是新的,有可能是整体的重新加载一遍
        new_chunk = self.splitter.split(self.documents,self.embedding)
        observer_updated = DocWatcherUpdatedFactory.createDocUpdatedPattern(pattern)
        observer_updated.execute(self.db, new_chunk)


    def get_retriever(self):
        current_chunks = self.splitter.split(self.documents, self.embedding)
        return RetrieverFactory.create_rewrite_retriever(RetrieverFactory.create_ensemble_retriever(self.db.get_retriever(), current_chunks), self.llm)
    def get_async_retriever(self):
        current_chunks = self.splitter.split(self.documents, self.embedding)
        return RetrieverFactory.create_ensemble_retriever(self.db.get_retriever(), current_chunks)

    def create_retriever(self,is_async):
        """统一检索器创建逻辑"""
        base_retriever = self.get_async_retriever() if is_async else self.get_retriever()
        if use_rerank:
            return RetrieverFactory.create_rerank_retriever(base_retriever)  #待完善
        return base_retriever

