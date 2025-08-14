from langchain_core.prompts import ChatPromptTemplate
from GitHub_Prepared_Rag.Core.factories.llm_factory import *
from GitHub_Prepared_Rag.Core.embedding_utils import embedding
from .document_utils import *
from GitHub_Prepared_Rag.Core.factories.db_factory import DBFactory
from GitHub_Prepared_Rag.Core.factories.update_strategy_factory import StrategyFactory
from GitHub_Prepared_Rag.Core.factories.splitter_factory import SplitterFactory
from GitHub_Prepared_Rag.Core.factories.retriever_factory import RetrieverFactory
from .observe_pattern import Observer
class RagManager(Observer):
    def __init__(self):
        self.embedding = embedding()
        self.documents = load_doc()
        self.llm = LLMFactory.create_llm()
        self.db = DBFactory.create_db(self.embedding)
        self.update_strategy = StrategyFactory.create_strategy()
        self.update_strategy.execute(self.db,self.documents)

        self.splitter = SplitterFactory.create_splitter()
        self.chunk = self.splitter.split(self.documents,self.embedding)
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
    def update(self, docs):
        self.documents = docs
        self.chunk = self.splitter.split(self.documents,self.embedding)
        StrategyFactory.Update_database().execute(self.db,self.chunk)

    def get_retriever(self):
        return RetrieverFactory.create_rewrite_retriever(RetrieverFactory.create_ensemble_retriever(self.db.get_retriever(), self.chunk), self.llm)
    def get_async_retriever(self):
        return RetrieverFactory.create_ensemble_retriever(self.db.get_retriever(), self.chunk)

    def create_retriever(self,is_async):
        """统一检索器创建逻辑"""
        base_retriever = self.get_async_retriever() if is_async else self.get_retriever()
        return base_retriever

