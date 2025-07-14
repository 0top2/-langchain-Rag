from langchain_community.chat_message_histories import RedisChatMessageHistory
from GitHub_Prepared_Rag.config import redis_url
def get_session_history(session_id):
    return RedisChatMessageHistory(session_id, url=redis_url)