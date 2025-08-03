from langchain_community.chat_message_histories import RedisChatMessageHistory
from GitHub_Prepared_Rag.Config.config import redis_url
def get_session_history(session_id:str):
    return RedisChatMessageHistory(session_id, url=redis_url)