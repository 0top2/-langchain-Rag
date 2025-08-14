from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda

from .RAGManager import RagManager
from GitHub_Prepared_Rag.Utils.get_session_history import get_session_history
from GitHub_Prepared_Rag.Utils.format_doc import format_doc


class Window():
    def __init__(self,*,manager:RagManager,id,is_async = False):
        self.id = id
        self.embedding = manager.embedding
        self.chunk = manager.chunk
        self.llm = manager.llm
        self.db = manager.db
        self.retriever = manager.create_retriever(is_async=is_async)
        self.chain = self.chain = {"context": RunnableLambda(lambda x: x['input']) | self.retriever | format_doc,
                      "history": RunnableLambda(lambda x: x['history']),
                      "input": RunnableLambda(lambda x: x['input'])} | manager.prompt | self.llm
        self.chain_with_history = RunnableWithMessageHistory(
                                  self.chain,
                                  get_session_history,
                                  input_messages_key="input",
                                  history_messages_key="history"
    )

    async def run(self,query):
        result = self.chain_with_history.invoke({"input": query},
                                                {"configurable":
                                                     {'session_id': self.id}
                                                 })
        print(f"AI:{result.content}")
    async def run_api(self,query):
        result = await self.chain_with_history.ainvoke({"input": query},
                                                {"configurable":
                                                     {'session_id': self.id}
                                                 })
        return result.content
