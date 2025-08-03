from dotenv import load_dotenv, find_dotenv
import os
import openai
from langchain_openai import ChatOpenAI
def llm():
    _ = load_dotenv(find_dotenv())
    openai.api_key = os.environ['OPENAI_API_KEY']
    openai.base_url = os.environ['OPENAI_API_URL']
    llm = ChatOpenAI(base_url=openai.base_url,
                     api_key=openai.api_key,
                     model='gpt-3.5-turbo')
    return llm





