from dotenv import load_dotenv, find_dotenv
import os
import openai
from langchain_community.chat_models import ChatZhipuAI, ChatSparkLLM
from langchain_openai import ChatOpenAI
from GitHub_Prepared_Rag.Config.config import *
def llm():
    if llm_type =='openai':
        _ = load_dotenv(find_dotenv())
        openai.api_key = os.environ['OPENAI_API_KEY']
        openai.base_url = os.environ['OPENAI_API_URL']
        llm = ChatOpenAI(base_url=openai.base_url,
                         api_key=openai.api_key,
                         model='gpt-3.5-turbo')
    elif llm_type =='zhipuai':
        llm = ChatZhipuAI(model='GLM-4-Flash-250414',
                          api_key=zhipu_api_key
                          )
    elif llm_type =='spark':
        llm = ChatSparkLLM(
            spark_app_id=spark_api_id,
            spark_api_key=spark_api_key,
            spark_api_secret=spark_api_secret,
            model="lite",  # 明确指定使用Lite模型
            spark_api_url="wss://spark-api.xf-yun.com/v1.1/chat",  # Lite版本对应的WebSocket地址
            spark_llm_domain="lite",  # 领域参数需与模型匹配
        )
    return llm





