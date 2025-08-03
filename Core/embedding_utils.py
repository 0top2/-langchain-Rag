from langchain.embeddings import CacheBackedEmbeddings
from langchain_community.storage import RedisStore
from langchain_huggingface import HuggingFaceEmbeddings
from GitHub_Prepared_Rag.Config.config import *

def embedding(model_name = "BAAI/bge-large-en-v1.5"):
    option = input("请问模型是否从网上加载:Y/N")
    if option in ['Y', 'y']:
        try:
            embedding = HuggingFaceEmbeddings(model_name=model_name,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )
        except Exception as e:
            print("远程加载模型失败,正在从本地加载....")
            embedding = HuggingFaceEmbeddings(model_name = embedding_url,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )
        return embedding
    return HuggingFaceEmbeddings(model_name = embedding_url,
                                          encode_kwargs={
                                              'normalize_embeddings': True
                                          }
                                          )

def cache_embedding(embedding):
    store = RedisStore(redis_url=redis_url, namespace="vector")
    # embedding = SentenceTransformer("BAAI/bge-large-en-v1.5")
    cache = CacheBackedEmbeddings.from_bytes_store(
        underlying_embeddings=embedding,
        document_embedding_cache=store,
        key_encoder="sha256"
    )
    return cache