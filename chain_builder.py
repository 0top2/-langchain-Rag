from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableWithMessageHistory, RunnableLambda
from Utils.get_session_history import get_session_history
from Utils.format_doc import format_doc
from data_preparing import doc_process,embedding,llm,cache_embedding,Retriever,query_rewrite_retriever,index_change_db
class Window():
    def __init__(self,ID,embedding,cache):
        self.id = ID
        self.embedding = embedding
        self.chunk = doc_process(self.embedding)
        self.llm = llm()
        self.cache = cache
        self.db = index_change_db(self.chunk,self.cache)
        self.retriever = query_rewrite_retriever(Retriever(self.db.as_retriever(),self.chunk),self.llm)
        self.prompt =ChatPromptTemplate.from_messages([
            ('system','你是一个专业的文档信息解读专家,请你根据文档里的内容和历史记录并结合一些常识来回答用户的问题,不用过于严谨,只输出答案,不要多余内容'
                      '文档内容:`{context}`'
                            
                      '历史记录:`{history}`'),
            ('user','{input}')
        ])
        self.chain = {"context":RunnableLambda(lambda x:x['input'])|self.retriever|format_doc,
                      "history":RunnableLambda(lambda x:x['history']),
                      "input":RunnableLambda(lambda x:x['input'])} |self.prompt|self.llm
        self.chain_with_history = RunnableWithMessageHistory(
                                  self.chain,
                                  get_session_history,
                                  input_messages_key="input",
                                  history_messages_key="history"
    )
    async def arun(self,query):
        result = self.chain_with_history.stream({"input":query},
                                        {"configurable":
                                                        {'session_id':self.id}
                                              })
        print("AI:",end="",flush=True)
        async for i in result:
            print(i.content,end="",flush=True)
        print()

    async def run(self,query):
        result = self.chain_with_history.invoke({"input": query},
                                                {"configurable":
                                                     {'session_id': self.id}
                                                 })
        print(f"AI:{result.content}")
    async def run_api(self,query):
        result = self.chain_with_history.invoke({"input": query},
                                                {"configurable":
                                                     {'session_id': self.id}
                                                 })
        return result.content
