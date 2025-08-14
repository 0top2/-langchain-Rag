from GitHub_Prepared_Rag.Config.config import *
from ..abstraction_base.llm_base import LLM
class OpenAI(LLM):
    def create_llm(self,config):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(**config)

class ZhipuAI(LLM):
    def create_llm(self,config):
        from langchain_community.chat_models import ChatZhipuAI
        return ChatZhipuAI(**config)

class Spark(LLM):
    def create_llm(self,config):
        from langchain_community.chat_models import ChatSparkAI
        return ChatSparkAI(**config)






