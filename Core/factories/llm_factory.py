from GitHub_Prepared_Rag.Config.config import *
from ..implementations.llm_implement import *
class LLMFactory:
    @staticmethod
    def create_llm():
        if llm_type == 'openai':
            return OpenAI().create_llm(llm_config)
        elif llm_type == 'zhipuai':
            return ZhipuAI().create_llm(llm_config)
        elif llm_type == 'spark':
            return Spark().create_llm(llm_config)